"""
Graph RAG System for PDDL QA Bot
"""
import logging
from typing import List, Dict, Any
from langchain.chat_models import init_chat_model
from knowledge_graph_qa import PDDLKnowledgeGraphQA
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download required NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDDLGraphRAGQA:
    """Graph RAG system for PDDL QA"""
    
    def __init__(self, knowledge_graph: PDDLKnowledgeGraphQA, cohere_api_key: str):
        self.kg = knowledge_graph
        self.cohere_api_key = cohere_api_key
        
        # Initialize Cohere chat model
        self.chat_model = init_chat_model(
            "command-r-plus", 
            model_provider="cohere", 
            api_key=cohere_api_key
        )
        
        # Initialize text processing
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        
        # BM25 corpus for keyword search
        self.bm25_corpus = []
        self.bm25_metadata = []
        self.bm25_model = None
        
        self._index_knowledge_base()
    
    def _preprocess_text(self, text: str) -> List[str]:
        """Preprocess text for BM25"""
        tokens = word_tokenize(text.lower())
        tokens = [self.stemmer.stem(token) for token in tokens 
                 if token.isalnum() and token not in self.stop_words]
        return tokens
    
    def _index_knowledge_base(self):
        """Index knowledge base for BM25 search"""
        logger.info("Indexing knowledge base for BM25 search...")
        
        # Get all domains, actions, and predicates for BM25 indexing
        domains = self.kg.get_all_domains()
        
        for domain in domains:
            # Index domain
            domain_text = f"{domain['name']} {domain['description']}"
            self.bm25_corpus.append(self._preprocess_text(domain_text))
            self.bm25_metadata.append({
                'type': 'Domain',
                'name': domain['name'],
                'description': domain['description']
            })
            
            # Index actions for this domain
            actions = self.kg.get_actions_by_domain(domain['name'])
            for action in actions:
                action_text = f"{action['name']} {action['description']} {' '.join(action.get('parameters', []))}"
                self.bm25_corpus.append(self._preprocess_text(action_text))
                self.bm25_metadata.append({
                    'type': 'Action',
                    'name': action['name'],
                    'description': action['description'],
                    'domain': domain['name']
                })
            
            # Index predicates for this domain
            predicates = self.kg.get_predicates_by_domain(domain['name'])
            for predicate in predicates:
                pred_text = f"{predicate['name']} {predicate['description']} {' '.join(predicate.get('parameters', []))}"
                self.bm25_corpus.append(self._preprocess_text(pred_text))
                self.bm25_metadata.append({
                    'type': 'Predicate',
                    'name': predicate['name'],
                    'description': predicate['description'],
                    'domain': domain['name']
                })
        
        # Build BM25 model
        if self.bm25_corpus:
            self.bm25_model = BM25Okapi(self.bm25_corpus)
            logger.info(f"Indexed {len(self.bm25_corpus)} items for BM25 search")
        else:
            logger.warning("No content available for BM25 indexing")
    
    def hybrid_retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Hybrid retrieval combining BM25 and semantic search"""
        all_results = []
        
        # BM25 retrieval
        if self.bm25_model:
            query_tokens = self._preprocess_text(query)
            bm25_scores = self.bm25_model.get_scores(query_tokens)
            
            # Get top BM25 results
            bm25_indices = sorted(range(len(bm25_scores)), 
                                key=lambda i: bm25_scores[i], reverse=True)[:top_k]
            
            for idx in bm25_indices:
                if bm25_scores[idx] > 0:
                    result = self.bm25_metadata[idx].copy()
                    result['score'] = float(bm25_scores[idx])
                    result['retrieval_type'] = 'BM25'
                    all_results.append(result)
        
        # Semantic similarity retrieval  
        semantic_results = self.kg.similarity_search(query, top_k)
        for result in semantic_results:
            node = result['node']
            similarity = result['similarity']
            labels = result['labels']
            
            semantic_result = {
                'type': labels[0] if labels else 'Unknown',
                'name': node.get('name', 'Unknown'),
                'description': node.get('description', ''),
                'score': float(similarity),
                'retrieval_type': 'Semantic'
            }
            
            if 'domain_name' in node:
                semantic_result['domain'] = node['domain_name']
                
            all_results.append(semantic_result)
        
        # Combine and deduplicate results
        seen = set()
        final_results = []
        for result in sorted(all_results, key=lambda x: x['score'], reverse=True):
            key = (result['type'], result['name'])
            if key not in seen:
                seen.add(key)
                final_results.append(result)
                if len(final_results) >= top_k:
                    break
        
        return final_results
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question about PDDL"""
        try:
            # Retrieve relevant context
            retrieved_results = self.hybrid_retrieve(question, top_k=5)
            
            if not retrieved_results:
                return {
                    'answer': "I don't have enough information to answer that question about PDDL. Could you try rephrasing your question?",
                    'context': [],
                    'confidence': 0.0
                }
            
            # Build context for the LLM
            context_parts = []
            for result in retrieved_results:
                context_part = f"**{result['type']}: {result['name']}**\n{result['description']}"
                if 'domain' in result:
                    context_part += f"\n(Domain: {result['domain']})"
                context_parts.append(context_part)
            
            context_text = "\n\n".join(context_parts)
            
            # Create prompt
            prompt = f"""You are an expert PDDL (Planning Domain Definition Language) assistant. Answer the following question using the provided context from the PDDL knowledge base.

Question: {question}

Context from PDDL Knowledge Base:
{context_text}

Instructions:
- Provide a clear, helpful answer about PDDL concepts
- Use the context information to support your answer
- If the question is about specific domains (blocks, gripper, logistics), reference them
- Include practical examples when helpful
- Be concise but informative

Answer:"""

            # Generate response
            response = self.chat_model.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            # Calculate confidence based on retrieval scores
            avg_score = sum(r['score'] for r in retrieved_results) / len(retrieved_results)
            confidence = min(avg_score, 1.0)
            
            return {
                'answer': answer,
                'context': retrieved_results,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                'answer': f"I encountered an error while processing your question: {str(e)}",
                'context': [],
                'confidence': 0.0
            }
    
    def get_sample_questions(self) -> List[str]:
        """Get sample questions for the interface"""
        return [
            "How do I pick up objects in PDDL?",
            "What is the difference between preconditions and effects?",
            "How does the blocks world domain work?",
            "What are predicates in PDDL?",
            "How do I define actions in a planning domain?",
            "What is the gripper domain used for?",
            "How do I specify object types in PDDL?",
            "What are the main components of a PDDL domain file?"
        ]
