import os
import time
from dotenv import load_dotenv
from pinecone import ServerlessSpec, Pinecone as pc
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
import cohere
import subprocess
import json
import re

load_dotenv()

# Configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "rag-knowledge"
KNOWLEDGE_FILE = "rag_knowledge.txt"

# Smaller chunking parameters for tiny documents
CHUNK_SIZE = 100  # Much smaller
CHUNK_OVERLAP = 20

def load_single_document(filepath: str) -> Document:
    """Load a single text document"""
    if not os.path.exists(filepath):
        print(f"File '{filepath}' does not exist.")
        return None
        
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
        document = Document(
            page_content=content,
            metadata={
                "source": os.path.basename(filepath),
                "type": "rag_knowledge",
                "filename": filepath
            }
        )
        
        print(f"Loaded document: {filepath}")
        print(f"Content length: {len(content)} characters")
        print(f"Content preview: {content[:200]}")  # Show content
        return document
        
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def create_and_store_embeddings(document: Document, pinecone_index_name: str, embeddings_model: CohereEmbeddings):
    """Create chunks and store embeddings in Pinecone"""
    print("Setting up chunking and embedding storage...")

    # Define text splitter with more separators
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ": ", ", ", " ", ""],  # More separators
        length_function=len
    )

    pine_client = pc(api_key=PINECONE_API_KEY)

    # Check if index exists and delete it to start fresh
    existing_indexes = pine_client.list_indexes().names()
    if pinecone_index_name in existing_indexes:
        print(f"Deleting existing index '{pinecone_index_name}'...")
        pine_client.delete_index(pinecone_index_name)
        time.sleep(5)  # Wait for deletion

    # Create fresh index
    print("Creating new Pinecone index...")
    pine_client.create_index(
        name=pinecone_index_name,
        metric="cosine",
        dimension=1024,  # Cohere embed-english-v3.0 dimension
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
    )
    print(f"Index '{pinecone_index_name}' created successfully!")
    time.sleep(15)  # Wait longer for index to be ready

    # Initialize Pinecone vector store
    vectorstore = PineconeVectorStore(
        index_name=pinecone_index_name,
        embedding=embeddings_model
    )

    # Split document into chunks
    chunks = text_splitter.split_documents([document])
    print(f"\nCreated {len(chunks)} chunks from the document")
    
    # If no chunks created, create one manually from full content
    if len(chunks) == 0:
        print("No chunks created by splitter. Creating chunk from full document...")
        chunks = [document]  # Use the whole document as one chunk
    
    # Display all chunks for verification
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ({len(chunk.page_content)} chars) ---")
        print(f"Content: '{chunk.page_content}'")
        print(f"Metadata: {chunk.metadata}")

    # Add to vectorstore with retry
    try:
        print(f"\nAdding {len(chunks)} chunks to Pinecone...")
        vectorstore.add_documents(chunks)
        print(f"Successfully added {len(chunks)} chunks to Pinecone!")
        
        # Wait a bit for indexing
        print("Waiting for indexing to complete...")
        time.sleep(10)
        
        # Verify the documents were added
        index = pine_client.Index(pinecone_index_name)
        stats = index.describe_index_stats()
        print(f"Index stats: {stats}")
        
    except Exception as e:
        print(f"Error adding documents to Pinecone: {e}")
        raise

    return vectorstore

def test_retrieval(vectorstore):
    """Test the retrieval system with relevant queries"""
    test_queries = [
        "Missing",
        "parentheses", 
        "error",
        "31",
        "ACTION"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing query: '{query}'")
        print('='*60)
        
        try:
            # Try different search methods
            print("Method 1: Using retriever...")
            retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
            retrieved_docs = retriever.get_relevant_documents(query)
            print(f"Retriever found {len(retrieved_docs)} documents")
            
            print("\nMethod 2: Using similarity search...")
            similar_docs = vectorstore.similarity_search(query, k=5)
            print(f"Similarity search found {len(similar_docs)} documents")
            
            print("\nMethod 3: Using similarity search with scores...")
            similar_docs_with_scores = vectorstore.similarity_search_with_score(query, k=5)
            print(f"Similarity search with scores found {len(similar_docs_with_scores)} documents")
            
            # Display results from the method that found documents
            docs_to_display = retrieved_docs or similar_docs
            if similar_docs_with_scores and not docs_to_display:
                docs_to_display = [doc for doc, score in similar_docs_with_scores]
            
            if docs_to_display:
                for i, doc in enumerate(docs_to_display):
                    print(f"\n--- Result {i+1} ---")
                    print(f"Source: {doc.metadata.get('source', 'N/A')}")
                    print(f"Content: '{doc.page_content}'")
                    if similar_docs_with_scores and i < len(similar_docs_with_scores):
                        print(f"Score: {similar_docs_with_scores[i][1]}")
                    print("-" * 30)
            else:
                print("No documents found with any method!")
                
        except Exception as e:
            print(f"Error during retrieval: {e}")

def run_llm_ic_pddl(task_id: int, run: int, time_limit: int = 200):
    """Run the original llm_ic_pddl method and return results"""
    print(f"Running llm_ic_pddl for task {task_id}, run {run}...")
    
    try:
        # Run the main.py with llm_ic_pddl method
        cmd = [
            "python", "main.py", 
            "--method", "llm_ic_pddl",
            "--task", str(task_id),
            "--run", str(run),
            "--time-limit", str(time_limit)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        # Parse the output for errors
        stdout = result.stdout
        stderr = result.stderr
        exit_code = result.returncode
        
        print(f"llm_ic_pddl completed with exit code: {exit_code}")
        
        # Try to find the log file
        log_pattern = f"./logs/run{run}/task_{task_id}_llm_ic_pddl*.json"
        import glob
        log_files = sorted(glob.glob(log_pattern), key=os.path.getmtime, reverse=True)
        
        log_data = None
        if log_files:
            with open(log_files[0], 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        
        return {
            "success": exit_code == 0 and log_data and log_data.get("plan_found", False),
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
            "log_data": log_data,
            "log_file": log_files[0] if log_files else None
        }
        
    except Exception as e:
        print(f"Error running llm_ic_pddl: {e}")
        return {
            "success": False,
            "exit_code": -1,
            "error": str(e),
            "log_data": None
        }

def extract_error_reason(log_data: dict, stdout: str, stderr: str) -> str:
    """Extract the main error reason from the planning attempt"""
    error_reasons = []
    
    # Check planner output for common errors
    if log_data:
        planner_output = log_data.get("planner_output", "")
        if "Missing ')'" in planner_output:
            error_reasons.append("Missing closing parenthesis")
        if "Tokens remaining after parsing" in planner_output:
            error_reasons.append("Extra text after PDDL")
        if "exit code: 31" in planner_output:
            error_reasons.append("PDDL syntax error")
        if "exit code: 37" in planner_output:
            error_reasons.append("Unsolvable problem")
            
        # Check for zero-step plan
        if log_data.get("plan_found") and "Plan length: 0 step(s)" in planner_output:
            error_reasons.append("Goal already satisfied")
    
    # Check stdout/stderr
    if "Missing ')'" in stdout or "Missing ')'" in stderr:
        error_reasons.append("Missing closing parenthesis")
    if "Tokens remaining" in stdout or "Tokens remaining" in stderr:
        error_reasons.append("Extra text after PDDL")
    
    return " | ".join(error_reasons) if error_reasons else "Unknown error"

def query_rag_for_solution(error_reason: str, vectorstore: PineconeVectorStore) -> str:
    """Query the RAG knowledge base for solutions to the error"""
    print(f"Querying RAG knowledge base for: {error_reason}")
    
    try:
        # Search for relevant knowledge
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        retrieved_docs = retriever.get_relevant_documents(error_reason)
        
        print(f"Found {len(retrieved_docs)} relevant knowledge entries")
        
        # Extract actions/solutions from retrieved docs
        context = ""
        for i, doc in enumerate(retrieved_docs):
            print(f"Retrieved knowledge {i+1}: {doc.page_content}")
            context += f"Knowledge {i+1}: {doc.page_content}\n\n"
        
        return context if context.strip() else "No specific knowledge found"
        
    except Exception as e:
        print(f"Error querying RAG: {e}")
        return "Error accessing knowledge base"

def regenerate_problem_with_cohere(original_problem: str, domain_content: str, error_reason: str, rag_context: str, task_id: int) -> str:
    """Use Cohere LLM to regenerate the problem file based on RAG knowledge"""
    print("Regenerating problem file using Cohere LLM...")
    
    try:
        cohere_client = cohere.Client(api_key=COHERE_API_KEY)
        
        prompt = f"""You are a PDDL (Planning Domain Definition Language) expert. I need you to fix a PDDL problem file that has errors.

DOMAIN CONTENT:
{domain_content[:2000]}

ORIGINAL PROBLEM (WITH ERRORS):
{original_problem}

ERROR DETECTED: {error_reason}

KNOWLEDGE FROM RAG DATABASE:
{rag_context}

TASK: Please regenerate the PROBLEM file only, ensuring:
1. Proper parentheses matching (every '(' has a corresponding ')')
2. No extra text after the final closing parenthesis
3. Valid PDDL syntax
4. Keep the same problem structure and goals

IMPORTANT: Return ONLY the corrected PROBLEM PDDL content, starting with (define and ending with the final ). Do not include any explanations or extra text.

CORRECTED PROBLEM:"""

        response = cohere_client.chat(
            model="command-r-plus",
            message=prompt,
            temperature=0.1,  # Low temperature for consistent fixes
            max_tokens=1500,
            p=0.95
        )
        
        corrected_problem = response.text.strip()
        
        # Basic validation - ensure it starts and ends correctly
        if not corrected_problem.startswith("(define"):
            print("Warning: Generated problem doesn't start with (define")
        if not corrected_problem.endswith(")"):
            print("Warning: Generated problem doesn't end with )")
            
        print("Problem regenerated successfully")
        return corrected_problem
        
    except Exception as e:
        print(f"Error regenerating problem with Cohere: {e}")
        return original_problem  # Return original if regeneration fails

if __name__ == "__main__":
    print("Starting single document processing...")
    
    # Initialize embeddings
    embeddings = CohereEmbeddings(model="embed-english-v3.0")
    
    # Load the single document
    document = load_single_document(KNOWLEDGE_FILE)

    if not document:
        print(f"Could not load document '{KNOWLEDGE_FILE}'. Please check the file exists.")
    else:
        print(f"Processing document: {KNOWLEDGE_FILE}")
        
        # Process and store in Pinecone
        vectorstore = create_and_store_embeddings(
            document, 
            PINECONE_INDEX_NAME, 
            embeddings
        )
        
        # Test retrieval
        test_retrieval(vectorstore)
        
        print("\n" + "="*60)
        print("RAG KNOWLEDGE BASE SETUP COMPLETED")
        print("Use llm_ic_pddl_rag method in main.py to test the system")
        print("="*60)

    print("\nDocument processing completed!")