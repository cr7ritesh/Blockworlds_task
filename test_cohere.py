import os
import time
from dotenv import load_dotenv
import cohere

# Load environment variables
load_dotenv()

def test_basic_cohere_connection():
    """Test basic Cohere API connection"""
    print("=" * 50)
    print("Testing Basic Cohere Connection")
    print("=" * 50)
    
    try:
        # Initialize Cohere client
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            print("❌ COHERE_API_KEY not found in environment variables")
            return False
            
        client = cohere.Client(api_key)
        print(f"✅ API Key loaded: {api_key[:8]}...")
        
        # Test simple query
        response = client.chat(
            model="command-r-plus",
            message="Hello, can you respond with just 'Hello World'?",
            temperature=0.0,
            max_tokens=50
        )
        
        print(f"✅ Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_planner_class():
    """Test the Planner class from main.py"""
    print("\n" + "=" * 50)
    print("Testing Planner Class")
    print("=" * 50)
    
    try:
        # Import the Planner class
        from main import Planner
        
        planner = Planner()
        print("✅ Planner initialized successfully")
        
        # Test a simple query
        test_prompt = "What is 2+2? Respond with just the number."
        response = planner.query(test_prompt)
        print(f"✅ Query response: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_blocksworld_domain():
    """Test loading the blocksworld domain"""
    print("\n" + "=" * 50)
    print("Testing Blocksworld Domain")
    print("=" * 50)
    
    try:
        from main import Blocksworld
        
        domain = Blocksworld()
        print(f"✅ Domain loaded: {domain.name}")
        print(f"✅ Number of tasks: {len(domain)}")
        
        if len(domain) > 0:
            # Test getting a task
            task_nl, task_pddl = domain.get_task(0)
            print(f"✅ First task loaded")
            print(f"   Natural Language (first 100 chars): {task_nl[:100]}...")
            print(f"   PDDL (first 100 chars): {task_pddl[:100]}...")
            
            # Test getting context
            context_nl, _, _ = domain.get_context()
            print(f"✅ Context loaded")
            print(f"   Context NL (first 50 chars): {context_nl[:50]}...")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prompt_generation():
    """Test prompt generation methods"""
    print("\n" + "=" * 50)
    print("Testing Prompt Generation")
    print("=" * 50)
    
    try:
        from main import Planner, Blocksworld
        
        planner = Planner()
        domain = Blocksworld()
        
        if len(domain) > 0:
            task_nl, _ = domain.get_task(0)
            domain_nl = domain.get_domain_nl()
            context = domain.get_context()
            
            # Test different prompt types
            llm_prompt = planner.create_llm_prompt(task_nl, domain_nl)
            print(f"✅ LLM prompt generated (length: {len(llm_prompt)})")
            
            llm_ic_prompt = planner.create_llm_ic_prompt(task_nl, domain_nl, context)
            print(f"✅ LLM IC prompt generated (length: {len(llm_ic_prompt)})")
            
            llm_pddl_prompt = planner.create_llm_pddl_prompt(task_nl, domain_nl)
            print(f"✅ LLM PDDL prompt generated (length: {len(llm_pddl_prompt)})")
            
            llm_ic_pddl_prompt = planner.create_llm_ic_pddl_prompt(task_nl, domain_nl, context)
            print(f"✅ LLM IC PDDL prompt generated (length: {len(llm_ic_pddl_prompt)})")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_end_to_end_query():
    """Test end-to-end query with a simple PDDL generation task"""
    print("\n" + "=" * 50)
    print("Testing End-to-End PDDL Generation")
    print("=" * 50)
    
    try:
        from main import Planner, Blocksworld
        
        planner = Planner()
        domain = Blocksworld()
        
        if len(domain) > 0:
            task_nl, _ = domain.get_task(0)
            domain_nl = domain.get_domain_nl()
            
            print(f"Task: {task_nl[:100]}...")
            
            # Generate PDDL prompt and query
            prompt = planner.create_llm_pddl_prompt(task_nl, domain_nl)
            print(f"✅ Prompt generated (first 200 chars): {prompt[:200]}...")
            
            start_time = time.time()
            response = planner.query(prompt)
            end_time = time.time()
            
            print(f"✅ Response received in {end_time - start_time:.2f} seconds")
            print(f"✅ Response length: {len(response)} characters")
            print(f"Response preview (first 300 chars):\n{response[:300]}...")
            
            # Check if response looks like PDDL
            if "(define" in response.lower() and "problem" in response.lower():
                print("✅ Response appears to contain PDDL structure")
            else:
                print("⚠️  Response may not be valid PDDL")
                
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_variants():
    """Test different Cohere models"""
    print("\n" + "=" * 50)
    print("Testing Different Cohere Models")
    print("=" * 50)
    
    models_to_test = ["command-r", "command-r-plus"]
    api_key = os.getenv("COHERE_API_KEY")
    
    if not api_key:
        print("❌ No API key found")
        return False
        
    client = cohere.Client(api_key)
    test_message = "What is the capital of France? Answer in one word."
    
    for model in models_to_test:
        try:
            print(f"\nTesting {model}...")
            start_time = time.time()
            
            response = client.chat(
                model=model,
                message=test_message,
                temperature=0.0,
                max_tokens=50
            )
            
            end_time = time.time()
            print(f"✅ {model}: {response.text.strip()} (took {end_time - start_time:.2f}s)")
            return True
            
        except Exception as e:
            print(f"❌ {model} failed: {e}")

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Cohere Integration Tests")
    print("=" * 60)
    
    tests = [
        test_basic_cohere_connection,
        test_planner_class,
        test_blocksworld_domain,
        test_prompt_generation,
        test_end_to_end_query,
        test_model_variants
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test {test.__name__} has issues")
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Cohere integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()