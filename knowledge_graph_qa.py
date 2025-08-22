"""
Simplified Knowledge Graph for PDDL QA Bot
"""
import logging
from typing import List, Dict, Any
from neo4j import GraphDatabase
from langchain_cohere import CohereEmbeddings
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDDLKnowledgeGraphQA:
    """Simplified Knowledge Graph for PDDL QA"""
    
    def __init__(self, uri: str, username: str, password: str, cohere_api_key: str):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.embeddings = CohereEmbeddings(
            model="embed-english-v3.0",
            cohere_api_key=cohere_api_key
        )
        self._create_constraints_and_indices()
        
    def _create_constraints_and_indices(self):
        """Create necessary constraints and indices"""
        with self.driver.session() as session:
            # Constraints
            constraints = [
                "CREATE CONSTRAINT domain_name IF NOT EXISTS FOR (d:Domain) REQUIRE d.name IS UNIQUE",
                "CREATE CONSTRAINT action_name IF NOT EXISTS FOR (a:Action) REQUIRE a.name IS UNIQUE", 
                "CREATE CONSTRAINT predicate_name IF NOT EXISTS FOR (p:Predicate) REQUIRE p.name IS UNIQUE",
                "CREATE CONSTRAINT type_name IF NOT EXISTS FOR (t:Type) REQUIRE t.name IS UNIQUE"
            ]
            
            # Indices
            indices = [
                "CREATE INDEX domain_desc_index IF NOT EXISTS FOR (d:Domain) ON (d.description)",
                "CREATE INDEX action_desc_index IF NOT EXISTS FOR (a:Action) ON (a.description)",
                "CREATE INDEX predicate_desc_index IF NOT EXISTS FOR (p:Predicate) ON (p.description)"
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
            embedding = self.embeddings.embed_query(domain_text)
            
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
            embedding = self.embeddings.embed_query(action_text)
            
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
            embedding = self.embeddings.embed_query(pred_text)
            
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
            embedding = self.embeddings.embed_query(type_text)
            
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
    
    def similarity_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Perform semantic similarity search"""
        query_embedding = self.embeddings.embed_query(query)
        
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
