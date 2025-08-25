"""
Simplified Knowledge Graph for PDDL QA Bot
"""
import logging
import time
from typing import List, Dict, Any
from neo4j import GraphDatabase
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings as CommunityHuggingFaceEmbeddings
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDDLKnowledgeGraphQA:
    """Simplified Knowledge Graph for PDDL QA"""
    
    def __init__(self, uri: str, username: str, password: str, huggingface_token: str = None):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        # Try multiple embedding options
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
        except ImportError:
            try:
                # Fallback to community embeddings
                self.embeddings = CommunityHuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
            except ImportError:
                # Final fallback to simple text embeddings (using a hash-based approach)
                self.embeddings = None
                logger.warning("Could not load HuggingFace embeddings, using fallback method")
        self.last_api_call = 0  # Track last API call for rate limiting
        self._create_constraints_and_indices()
    
    def _rate_limit_delay(self):
        """Add delay for consistency (HuggingFace embeddings don't need rate limiting)"""
        current_time = time.time()
        time_since_last = current_time - self.last_api_call
        min_interval = 0.1  # Minimal delay for HuggingFace local embeddings
        
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_api_call = time.time()
        
    def _create_constraints_and_indices(self):
        """Create necessary constraints and indices"""
        with self.driver.session() as session:
            # Constraints
            constraints = [
                "CREATE CONSTRAINT domain_name IF NOT EXISTS FOR (d:Domain) REQUIRE d.name IS UNIQUE",
                "CREATE CONSTRAINT action_name IF NOT EXISTS FOR (a:Action) REQUIRE a.name IS UNIQUE", 
                "CREATE CONSTRAINT predicate_name IF NOT EXISTS FOR (p:Predicate) REQUIRE p.name IS UNIQUE",
                "CREATE CONSTRAINT type_name IF NOT EXISTS FOR (t:Type) REQUIRE t.name IS UNIQUE",
                "CREATE CONSTRAINT task_unique IF NOT EXISTS FOR (t:Task) REQUIRE (t.task_id, t.trial_id) IS UNIQUE",
                "CREATE CONSTRAINT initial_state_unique IF NOT EXISTS FOR (i:InitialState) REQUIRE (i.trial_id) IS UNIQUE"
            ]
            
            # Indices
            indices = [
                "CREATE INDEX domain_desc_index IF NOT EXISTS FOR (d:Domain) ON (d.description)",
                "CREATE INDEX action_desc_index IF NOT EXISTS FOR (a:Action) ON (a.description)",
                "CREATE INDEX predicate_desc_index IF NOT EXISTS FOR (p:Predicate) ON (p.description)",
                "CREATE INDEX task_type_index IF NOT EXISTS FOR (t:Task) ON (t.task_type)",
                "CREATE INDEX task_object_index IF NOT EXISTS FOR (t:Task) ON (t.target_object)"
            ]
            
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    logger.debug(f"Constraint creation: {e}")
                    
            for index in indices:
                try:
                    session.run(index)
                except Exception as e:
                    logger.debug(f"Index creation: {e}")
    
    def add_domain(self, domain_data):
        """Add a domain to the knowledge graph"""
        with self.driver.session() as session:
            # Create domain node with embedding
            domain_text = f"{domain_data.name} {domain_data.description}"
            self._rate_limit_delay()  # Add rate limiting delay
            if self.embeddings:
                embedding = self.embeddings.embed_query(domain_text)
            else:
                embedding = self._simple_text_embedding(domain_text)
            
            session.run("""
                MERGE (d:Domain {name: $name})
                SET d.description = $description,
                    d.file_path = $file_path,
                    d.num_actions = $num_actions,
                    d.num_predicates = $num_predicates,
                    d.num_types = $num_types,
                    d.embedding = $embedding
            """, {
                'name': domain_data.name,
                'description': domain_data.description,
                'file_path': domain_data.file_path,
                'num_actions': len(domain_data.actions),
                'num_predicates': len(domain_data.predicates),
                'num_types': len(domain_data.types),
                'embedding': embedding
            })
            
            logger.info(f"Added domain: {domain_data.name}")
    
    def add_action(self, action_data):
        """Add an action to the knowledge graph"""
        with self.driver.session() as session:
            # Create action text for embedding
            action_text = f"{action_data.name} {action_data.description} {' '.join(action_data.parameters)}"
            self._rate_limit_delay()  # Add rate limiting delay
            if self.embeddings:
                embedding = self.embeddings.embed_query(action_text)
            else:
                embedding = self._simple_text_embedding(action_text)
            
            session.run("""
                MERGE (a:Action {name: $name})
                SET a.description = $description,
                    a.parameters = $parameters,
                    a.preconditions = $preconditions,
                    a.effects = $effects,
                    a.domain_name = $domain_name,
                    a.embedding = $embedding
                
                // Link to domain
                WITH a
                MATCH (d:Domain {name: $domain_name})
                MERGE (d)-[:HAS_ACTION]->(a)
            """, {
                'name': action_data.name,
                'description': action_data.description,
                'parameters': action_data.parameters,
                'preconditions': action_data.preconditions,
                'effects': action_data.effects,
                'domain_name': action_data.domain_name,
                'embedding': embedding
            })
    
    def add_predicate(self, predicate_data):
        """Add a predicate to the knowledge graph"""
        with self.driver.session() as session:
            # Create predicate text for embedding
            pred_text = f"{predicate_data.name} {predicate_data.description} {' '.join(predicate_data.parameters)}"
            self._rate_limit_delay()  # Add rate limiting delay
            if self.embeddings:
                embedding = self.embeddings.embed_query(pred_text)
            else:
                embedding = self._simple_text_embedding(pred_text)
            
            session.run("""
                MERGE (p:Predicate {name: $name})
                SET p.description = $description,
                    p.parameters = $parameters,
                    p.domain_name = $domain_name,
                    p.embedding = $embedding
                
                // Link to domain
                WITH p
                MATCH (d:Domain {name: $domain_name})
                MERGE (d)-[:HAS_PREDICATE]->(p)
            """, {
                'name': predicate_data.name,
                'description': predicate_data.description,
                'parameters': predicate_data.parameters,
                'domain_name': predicate_data.domain_name,
                'embedding': embedding
            })
    
    def add_type(self, type_data):
        """Add a type to the knowledge graph"""
        with self.driver.session() as session:
            type_text = f"{type_data['name']} {type_data['description']}"
            if self.embeddings:
                embedding = self.embeddings.embed_query(type_text)
            else:
                embedding = self._simple_text_embedding(type_text)
            
            session.run("""
                MERGE (t:Type {name: $name})
                SET t.description = $description,
                    t.domain_name = $domain_name,
                    t.embedding = $embedding
                
                // Link to domain
                WITH t
                MATCH (d:Domain {name: $domain_name})
                MERGE (d)-[:HAS_TYPE]->(t)
            """, {
                'name': type_data['name'],
                'description': type_data['description'],
                'domain_name': type_data['domain_name'],
                'embedding': embedding
            })
    
    def add_task(self, task_data):
        """Add an ALFWORLD task to the knowledge graph"""
        with self.driver.session() as session:
            task_text = f"{task_data['task_type']} {task_data['target_object']} {task_data['toggle_target']} {task_data['description']}"
            self._rate_limit_delay()
            if self.embeddings:
                embedding = self.embeddings.embed_query(task_text)
            else:
                embedding = self._simple_text_embedding(task_text)
            
            session.run("""
                MERGE (t:Task {task_id: $task_id, trial_id: $trial_id})
                SET t.task_type = $task_type,
                    t.target_object = $target_object,
                    t.toggle_target = $toggle_target,
                    t.description = $description,
                    t.scene_num = $scene_num,
                    t.floor_plan = $floor_plan,
                    t.embedding = $embedding
            """, {
                'task_id': task_data['task_id'],
                'trial_id': task_data['trial_id'],
                'task_type': task_data['task_type'],
                'target_object': task_data['target_object'],
                'toggle_target': task_data['toggle_target'],
                'description': task_data['description'],
                'scene_num': task_data['scene_num'],
                'floor_plan': task_data['floor_plan'],
                'embedding': embedding
            })
    
    def add_initial_state(self, initial_state_data):
        """Add an ALFWORLD initial state to the knowledge graph"""
        with self.driver.session() as session:
            state_text = f"Initial state for {initial_state_data['trial_id']}: {' '.join(initial_state_data['predicates'][:10])}"
            self._rate_limit_delay()
            if self.embeddings:
                embedding = self.embeddings.embed_query(state_text)
            else:
                embedding = self._simple_text_embedding(state_text)
            
            session.run("""
                MERGE (i:InitialState {trial_id: $trial_id})
                SET i.predicates = $predicates,
                    i.objects = $objects,
                    i.locations = $locations,
                    i.receptacles = $receptacles,
                    i.embedding = $embedding
                
                // Link to task
                WITH i
                MATCH (t:Task {trial_id: $trial_id})
                MERGE (t)-[:HAS_INITIAL_STATE]->(i)
            """, {
                'trial_id': initial_state_data['trial_id'],
                'predicates': initial_state_data['predicates'],
                'objects': initial_state_data['objects'],
                'locations': initial_state_data['locations'],
                'receptacles': initial_state_data['receptacles'],
                'embedding': embedding
            })
    
    def similarity_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Perform semantic similarity search"""
        if self.embeddings:
            query_embedding = self.embeddings.embed_query(query)
        else:
            # Fallback: simple hash-based embedding
            query_embedding = self._simple_text_embedding(query)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                WHERE n.embedding IS NOT NULL
                WITH n, 
                     gds.similarity.cosine(n.embedding, $query_embedding) AS similarity
                WHERE similarity > 0.3
                RETURN n, similarity
                ORDER BY similarity DESC
                LIMIT $limit
            """, {
                'query_embedding': query_embedding,
                'limit': limit
            })
            
            results = []
            for record in result:
                node = record['n']
                similarity = record['similarity']
                
                results.append({
                    'node': dict(node),
                    'similarity': similarity,
                    'labels': list(node.labels)
                })
            
            return results
    
    def _simple_text_embedding(self, text: str) -> List[float]:
        """Simple fallback embedding using hash-based features"""
        import hashlib
        # Create a simple 128-dimensional embedding based on text features
        words = text.lower().split()
        embedding = [0.0] * 128
        
        # Hash-based features
        for i, word in enumerate(words[:32]):  # Use first 32 words
            hash_val = int(hashlib.md5(word.encode()).hexdigest()[:8], 16)
            for j in range(4):  # 4 dimensions per word
                idx = (i * 4 + j) % 128
                embedding[idx] = ((hash_val >> (j * 8)) & 0xFF) / 255.0
        
        # Text length features
        embedding[120] = min(len(text) / 1000.0, 1.0)
        embedding[121] = min(len(words) / 100.0, 1.0)
        
        # Character frequency features  
        for char in 'aeiou':
            idx = 122 + ord(char) - ord('a')
            if idx < 128:
                embedding[idx] = text.lower().count(char) / len(text) if text else 0.0
        
        return embedding
    
    def get_all_domains(self) -> List[Dict[str, Any]]:
        """Get all domains"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Domain)
                RETURN d.name AS name, d.description AS description,
                       d.num_actions AS num_actions, d.num_predicates AS num_predicates
                ORDER BY d.name
            """)
            
            return [dict(record) for record in result]
    
    def get_actions_by_domain(self, domain_name: str) -> List[Dict[str, Any]]:
        """Get all actions for a domain"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Domain {name: $domain_name})-[:HAS_ACTION]->(a:Action)
                RETURN a.name AS name, a.description AS description,
                       a.parameters AS parameters
                ORDER BY a.name
            """, {'domain_name': domain_name})
            
            return [dict(record) for record in result]
    
    def get_predicates_by_domain(self, domain_name: str) -> List[Dict[str, Any]]:
        """Get all predicates for a domain"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Domain {name: $domain_name})-[:HAS_PREDICATE]->(p:Predicate)
                RETURN p.name AS name, p.description AS description,
                       p.parameters AS parameters
                ORDER BY p.name
            """, {'domain_name': domain_name})
            
            return [dict(record) for record in result]
    
    def get_stats(self) -> Dict[str, int]:
        """Get knowledge graph statistics"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] AS node_type, count(n) AS count
            """)
            
            stats = {}
            total = 0
            for record in result:
                node_type = record['node_type']
                count = record['count']
                stats[node_type] = count
                total += count
            
            stats['total_nodes'] = total
            return stats
    
    def close(self):
        """Close the database connection"""
        if self.driver:
            self.driver.close()
