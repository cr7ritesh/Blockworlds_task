#!/usr/bin/env python3
"""
Add Error Information to Existing Knowledge Graph
"""
import os
import logging
from dotenv import load_dotenv
from kg_initializer import PDDLKnowledgeGraphInitializer

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_error_information():
    """Add error information to the existing KG"""
    try:
        print("\n" + "="*60)
        print("ADDING ERROR INFORMATION TO KNOWLEDGE GRAPH")
        print("="*60)
        
        # Initialize
        initializer = PDDLKnowledgeGraphInitializer()
        
        if not initializer.kg:
            print("[ERROR] Failed to initialize knowledge graph")
            return False
        
        print("\n[INFO] Adding error fixes from user table...")
        initializer.populate_error_fixes_from_user_table()
        
        print("\n[INFO] Verifying error data addition...")
        success, counts = initializer.verify_data_ingestion()
        
        if success:
            print("\n[SUCCESS] Error information added successfully!")
            print("\n[INFO] Updated Summary:")
            for node_type, count in counts.items():
                if count > 0:
                    print(f"  * {node_type}: {count}")
                    
            error_fix_count = counts.get('ErrorFix', 0)
            if error_fix_count > 0:
                print(f"\n[SUCCESS] Added {error_fix_count} error fixes to the Knowledge Graph!")
            else:
                print("\n[WARNING] No error fixes were added")
        else:
            print("\n[ERROR] Failed to add error information")
        
        return success
        
    except Exception as e:
        print(f"\n[ERROR] Error adding error information: {e}")
        return False
        
    finally:
        if 'initializer' in locals():
            initializer.close_connections()

if __name__ == "__main__":
    success = add_error_information()
    exit(0 if success else 1)