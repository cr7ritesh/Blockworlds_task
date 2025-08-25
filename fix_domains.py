#!/usr/bin/env python3
"""
Fix Domain Parsing and Add Alfred Domain
"""
import os
import logging
from dotenv import load_dotenv
from kg_initializer import PDDLKnowledgeGraphInitializer

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_domains():
    """Fix domain parsing and add Alfred domain"""
    try:
        print("\n" + "="*60)
        print("FIXING DOMAINS AND ADDING ALFRED DOMAIN")
        print("="*60)
        
        # Initialize
        initializer = PDDLKnowledgeGraphInitializer()
        
        if not initializer.kg:
            print("[ERROR] Failed to initialize knowledge graph")
            return False
        
        # Fix logistics domain parsing by processing it again
        print("\n[INFO] Re-processing all domains with improved parsing...")
        domain_paths = ["data/blocks", "data/gripper", "data/logistics"]
        initializer.populate_with_domains(domain_paths)
        
        # Add Alfred domain
        print("\n[INFO] Adding ALFWORLD Alfred domain...")
        alfred_path = "alfred.pddl"
        if os.path.exists(alfred_path):
            # Parse and add Alfred domain directly
            domain_data = initializer.parse_pddl_domain(alfred_path)
            initializer.kg.add_domain(domain_data)
            print("[SUCCESS] Alfred domain processed")
        else:
            print("[WARNING] alfred.pddl not found")
        
        print("\n[INFO] Verifying updated domains...")
        success, counts = initializer.verify_data_ingestion()
        
        if success:
            print("\n[SUCCESS] Domain fixes completed successfully!")
            print("\n[INFO] Updated Summary:")
            for node_type, count in counts.items():
                if count > 0:
                    print(f"  * {node_type}: {count}")
                    
            action_count = counts.get('Action', 0)
            domain_count = counts.get('Domain', 0)
            print(f"\n[INFO] Now have {domain_count} domains with {action_count} total actions")
        else:
            print("\n[ERROR] Domain verification failed")
        
        return success
        
    except Exception as e:
        print(f"\n[ERROR] Error fixing domains: {e}")
        return False
        
    finally:
        if 'initializer' in locals():
            initializer.close_connections()

if __name__ == "__main__":
    success = fix_domains()
    exit(0 if success else 1)