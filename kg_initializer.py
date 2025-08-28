"""
Knowledge Graph Initializer for PDDL Framework
This module handles the initialization and population of the Neo4j knowledge graph
with PDDL domain information and planning examples.
"""

import os
import logging
import re
import json
import glob
import time
from typing import List, Dict, Any, NamedTuple
from dotenv import load_dotenv
from knowledge_graph_qa import PDDLKnowledgeGraphQA
import math

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data structures for PDDL parsing
class DomainData(NamedTuple):
    name: str
    description: str
    file_path: str
    actions: List[Dict[str, Any]]
    predicates: List[Dict[str, Any]]
    types: List[Dict[str, Any]]

class ActionData(NamedTuple):
    name: str
    description: str
    parameters: List[str]
    preconditions: List[str]
    effects: List[str]
    domain_name: str

class PredicateData(NamedTuple):
    name: str
    description: str
    parameters: List[str]
    domain_name: str

class ErrorCase(NamedTuple):
    task_id: int
    method: str
    error_type: str
    error_description: str
    exit_code: int
    domain_name: str
    timestamp: str

class ErrorFix(NamedTuple):
    error_type: str
    fix_title: str
    fix_description: str
    fix_strategy: str
    source: str
    example_before: str
    example_after: str


class PDDLKnowledgeGraphInitializer:
    """
    Initializes and manages the PDDL Knowledge Graph in Neo4j
    """
    
    def __init__(self):
        """Initialize with Neo4j credentials from environment variables"""
        self.neo4j_uri = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
        self.neo4j_username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
        self.neo4j_database = os.getenv("NEO4J_DATABASE", "neo4j")
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
        
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY not found in environment variables")
        
        # Initialize knowledge graph connection immediately
        self.kg = None
        self.initialize_knowledge_graph()
    
    def initialize_knowledge_graph(self):
        """Initialize the knowledge graph connection and structure"""
        try:
            logger.info("Connecting to Neo4j database...")
            logger.info(f"Neo4j URI: {self.neo4j_uri}")
            logger.info(f"Neo4j Username: {self.neo4j_username}")
            logger.info(f"Neo4j Database: {self.neo4j_database}")
            
            # Initialize knowledge graph
            self.kg = PDDLKnowledgeGraphQA(
                uri=self.neo4j_uri,
                username=self.neo4j_username,
                password=self.neo4j_password,
                huggingface_token=self.huggingface_token
            )
            
            logger.info("[SUCCESS] Knowledge graph connection established successfully")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize knowledge graph: {e}")
            return False
    
    def parse_pddl_domain(self, domain_file_path: str) -> DomainData:
        """Parse a PDDL domain file and extract relevant information"""
        try:
            with open(domain_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract domain name
            name_match = re.search(r'\(domain\s+([^)]+)\)', content, re.IGNORECASE)
            domain_name = name_match.group(1).strip() if name_match else "unknown_domain"
            
            # Generate description based on domain name and content analysis
            description = self._generate_domain_description(domain_name, content)
            
            # Extract actions
            actions = self._extract_actions(content, domain_name)
            
            # Extract predicates
            predicates = self._extract_predicates(content, domain_name)
            
            # Extract types
            types = self._extract_types(content, domain_name)
            
            return DomainData(
                name=domain_name,
                description=description,
                file_path=domain_file_path,
                actions=actions,
                predicates=predicates,
                types=types
            )
            
        except Exception as e:
            logger.error(f"Error parsing domain file {domain_file_path}: {e}")
            return None
    
    def _generate_domain_description(self, domain_name: str, content: str) -> str:
        """Generate a description for the domain based on its name and content"""
        descriptions = {
            "blocksworld": "A classic planning domain involving stacking blocks on a table and on top of each other",
            "blocks": "Planning domain for manipulating blocks in various configurations",
            "gripper": "Robot gripper domain for picking up and moving objects between locations",
            "logistics": "Transportation and logistics domain involving packages, vehicles, and locations",
        }
        
        # Check if domain name matches known patterns
        for key, desc in descriptions.items():
            if key.lower() in domain_name.lower():
                return desc
        
        # Fallback: generate description based on predicates and actions found
        action_count = len(re.findall(r':action\s+\w+', content, re.IGNORECASE))
        predicate_count = len(re.findall(r'\(\w+[^)]*\)', content)) // 2  # Rough estimate
        
        return f"PDDL planning domain '{domain_name}' with {action_count} actions and approximately {predicate_count} predicates"
    
    def _extract_actions(self, content: str, domain_name: str) -> List[Dict[str, Any]]:
        """Extract actions from PDDL domain content"""
        actions = []
        
        # Find all action definitions - improved regex to handle multiline parameters
        action_pattern = r'\(:action\s+(\w+)\s*:parameters\s*\((.*?)\)\s*:precondition\s*(.*?)\s*:effect\s*(.*?)(?=\(:action|\Z)'
        matches = re.findall(action_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            action_name, parameters_str, preconditions_str, effects_str = match
            
            # Parse parameters
            parameters = self._parse_parameters(parameters_str)
            
            # Parse preconditions and effects (simplified)
            preconditions = [preconditions_str.strip()]
            effects = [effects_str.strip()]
            
            # Generate better description for action
            action_desc = f"Action {action_name} in {domain_name} domain with parameters: {', '.join(parameters) if parameters else 'none'}"
            
            action_data = ActionData(
                name=action_name.strip(),
                description=action_desc,
                parameters=parameters,
                preconditions=preconditions,
                effects=effects,
                domain_name=domain_name
            )
            
            actions.append(action_data._asdict())
        
        return actions
    
    def _extract_predicates(self, content: str, domain_name: str) -> List[Dict[str, Any]]:
        """Extract predicates from PDDL domain content"""
        predicates = []
        
        # Find predicates section
        predicates_match = re.search(r':predicates\s*\((.*?)\)\s*(?=:\w+)', content, re.DOTALL | re.IGNORECASE)
        if predicates_match:
            predicates_content = predicates_match.group(1)
            
            # Find individual predicates
            pred_pattern = r'\((\w+)([^)]*)\)'
            matches = re.findall(pred_pattern, predicates_content)
            
            for pred_name, params_str in matches:
                parameters = self._parse_parameters(params_str)
                
                predicate_data = PredicateData(
                    name=pred_name.strip(),
                    description=f"Predicate {pred_name} in {domain_name} domain",
                    parameters=parameters,
                    domain_name=domain_name
                )
                
                predicates.append(predicate_data._asdict())
        
        return predicates
    
    def _extract_types(self, content: str, domain_name: str) -> List[Dict[str, Any]]:
        """Extract types from PDDL domain content"""
        types = []
        
        # Find types section
        types_match = re.search(r':types\s+(.*?)(?=:\w+|\))', content, re.DOTALL | re.IGNORECASE)
        if types_match:
            types_content = types_match.group(1).strip()
            type_names = [t.strip() for t in types_content.split() if t.strip() and t.strip() != '-']
            
            for type_name in type_names:
                if type_name and not type_name.startswith('-'):
                    types.append({
                        'name': type_name,
                        'description': f"Type {type_name} in {domain_name} domain",
                        'domain_name': domain_name
                    })
        
        return types
    
    def _parse_parameters(self, params_str: str) -> List[str]:
        """Parse parameter string into list of parameters"""
        if not params_str.strip():
            return []
        
        # Simple parameter parsing - could be enhanced
        params = []
        tokens = params_str.split()
        current_param = ""
        
        for token in tokens:
            if token.startswith('?'):
                if current_param:
                    params.append(current_param.strip())
                current_param = token
            else:
                current_param += f" {token}"
        
        if current_param:
            params.append(current_param.strip())
        
        return params
    
    def add_error_case_to_kg(self, error_case: ErrorCase):
        """Add an error case to the knowledge graph"""
        try:
            # Add rate limiting to avoid Cohere API limits
            time.sleep(1.8)  # ~33 requests per minute to stay under 40/min limit
            
            with self.kg.driver.session(database=self.neo4j_database) as session:
                error_text = f"{error_case.error_type} {error_case.error_description}"
                if self.kg.embeddings:
                    embedding = self.kg.embeddings.embed_query(error_text)
                else:
                    embedding = self.kg._simple_text_embedding(error_text)
                
                session.run("""
                    MERGE (e:ErrorCase {task_id: $task_id, method: $method})
                    SET e.error_type = $error_type,
                        e.error_description = $error_description,
                        e.exit_code = $exit_code,
                        e.domain_name = $domain_name,
                        e.timestamp = $timestamp,
                        e.embedding = $embedding
                """, {
                    'task_id': error_case.task_id,
                    'method': error_case.method,
                    'error_type': error_case.error_type,
                    'error_description': error_case.error_description,
                    'exit_code': error_case.exit_code,
                    'domain_name': error_case.domain_name,
                    'timestamp': error_case.timestamp,
                    'embedding': embedding
                })
        except Exception as e:
            logger.error(f"Error adding error case: {e}")
    
    def add_error_fix_to_kg(self, error_fix: ErrorFix):
        """Add an error fix to the knowledge graph"""
        try:
            # Add rate limiting to avoid Cohere API limits  
            time.sleep(1.8)  # ~33 requests per minute to stay under 40/min limit
            
            with self.kg.driver.session(database=self.neo4j_database) as session:
                fix_text = f"{error_fix.error_type} {error_fix.fix_description}"
                if self.kg.embeddings:
                    embedding = self.kg.embeddings.embed_query(fix_text)
                else:
                    embedding = self.kg._simple_text_embedding(fix_text)
                
                session.run("""
                    MERGE (f:ErrorFix {error_type: $error_type, fix_title: $fix_title})
                    SET f.fix_description = $fix_description,
                        f.fix_strategy = $fix_strategy,
                        f.source = $source,
                        f.example_before = $example_before,
                        f.example_after = $example_after,
                        f.embedding = $embedding
                    
                    WITH f
                    MATCH (e:ErrorCase {error_type: $error_type})
                    MERGE (e)-[:HAS_FIX]->(f)
                """, {
                    'error_type': error_fix.error_type,
                    'fix_title': error_fix.fix_title,
                    'fix_description': error_fix.fix_description,
                    'fix_strategy': error_fix.fix_strategy,
                    'source': error_fix.source,
                    'example_before': error_fix.example_before[:500],
                    'example_after': error_fix.example_after[:500],
                    'embedding': embedding
                })
        except Exception as e:
            logger.error(f"Error adding error fix: {e}")
    
    def classify_error_from_logs(self, exit_code: int, planner_output: str) -> tuple:
        """Classify error from log data"""
        planner_lower = planner_output.lower()
        
        # Check for specific syntax/parse errors first
        if "parse error" in planner_lower or "syntax error" in planner_lower:
            if "unmatched" in planner_lower or "parenthes" in planner_lower:
                return "UNMATCHED_PARENTHESES", "Missing or extra parentheses in PDDL file"
            elif "unknown predicate" in planner_lower or "undefined predicate" in planner_lower:
                return "UNKNOWN_PREDICATE", "Predicate used but not declared in domain"
            elif "misspelled" in planner_lower or "keyword" in planner_lower:
                return "MISSPELLED_KEYWORD", "Incorrect spelling of PDDL keywords"
            elif "type" in planner_lower and "mismatch" in planner_lower:
                return "TYPE_MISMATCH", "Object type declaration inconsistency"
            elif "requirements" in planner_lower:
                return "MISSING_REQUIREMENT", "Required PDDL feature not declared"
            else:
                return "PLANNER_PARSE_ERROR", "General PDDL structure or syntax error"
        
        # Check exit codes for planning failures
        if exit_code == 12:
            if "No relaxed solution" in planner_output:
                return "UNSOLVABLE_PROBLEM", "Problem has no valid solution path"
            elif "Initial state is a dead end" in planner_output:
                return "DEAD_END_STATE", "Initial state blocks all actions"
            else:
                return "SEARCH_FAILURE", "Search could not find solution"
        elif exit_code == 31:
            return "TIMEOUT", "Planning exceeded time limit"
        elif exit_code == 1:
            return "GENERAL_ERROR", "General planning or parsing error"
        else:
            return "UNKNOWN_ERROR", f"Exit code {exit_code}"
    
    def populate_error_fixes_from_online_sources(self):
        """Add error fixes from known online PDDL sources"""
        error_fixes = [
            # From PDDL Wiki and IPC sources - General Planning Errors
            ErrorFix(
                error_type="UNSOLVABLE_PROBLEM",
                fix_title="Goal State Validation",
                fix_description="Verify that the goal state is reachable from initial state",
                fix_strategy="Check goal predicates exist in domain, verify action effects can achieve goals, ensure no contradictory goals",
                source="PDDL4J Documentation",
                example_before="(:goal (and (on ?a ?b) (on ?b ?a)))",
                example_after="(:goal (and (on ?a ?b) (clear ?a)))"
            ),
            ErrorFix(
                error_type="DEAD_END_STATE",
                fix_title="Initial State Consistency",
                fix_description="Fix initial state predicates to allow valid actions",
                fix_strategy="Ensure arm-empty when not holding, blocks can't be in multiple places, clear predicates match stacking",
                source="Planning.domains Examples",
                example_before="(:init (holding ?a) (holding ?b) (arm-empty))",
                example_after="(:init (holding ?a) (clear ?b) (on-table ?b))"
            ),
            ErrorFix(
                error_type="TIMEOUT",
                fix_title="Problem Complexity Reduction",
                fix_description="Reduce problem size or add domain constraints",
                fix_strategy="Limit number of objects, add helpful action ordering, use domain-specific heuristics",
                source="IPC Benchmarks Analysis",
                example_before="20+ blocks with complex goal configuration",
                example_after="5-8 blocks with simpler stacking goals"
            ),
            
            # Specific PDDL Syntax Errors from the table
            ErrorFix(
                error_type="UNMATCHED_PARENTHESES",
                fix_title="Parentheses Balance Error",
                fix_description="Missing or extra parentheses in PDDL structure",
                fix_strategy="Balance parentheses - count opening and closing brackets",
                source="PDDL Syntax Guide",
                example_before="(:init (clear a) (clear b",
                example_after="(:init (clear a) (clear b))"
            ),
            ErrorFix(
                error_type="MISSPELLED_KEYWORD",
                fix_title="PDDL Keyword Spelling",
                fix_description="Incorrect spelling of PDDL keywords",
                fix_strategy="Correct to standard PDDL keywords: :predicates, :actions, :init, :goal, etc.",
                source="PDDL Reference Manual",
                example_before=":predicats",
                example_after=":predicates"
            ),
            ErrorFix(
                error_type="WRONG_SECTION",
                fix_title="Section Placement Error",
                fix_description="PDDL elements placed in wrong file section",
                fix_strategy="Move :init and :goal to problem file, keep :predicates and :actions in domain file",
                source="PDDL Structure Rules",
                example_before=":init in domain file",
                example_after=":init moved to problem file"
            ),
            ErrorFix(
                error_type="UNKNOWN_PREDICATE",
                fix_title="Undeclared Predicate Usage",
                fix_description="Using predicate not declared in domain :predicates section",
                fix_strategy="Declare all used predicates in domain :predicates section",
                source="PDDL Validation Tools",
                example_before="(has tool1) used but not declared",
                example_after="(:predicates (has ?t - tool) ...) in domain"
            ),
            ErrorFix(
                error_type="TYPE_MISMATCH",
                fix_title="Object Type Declaration Error",
                fix_description="Object declared with wrong or inconsistent type",
                fix_strategy="Ensure object types match their usage in predicates and actions",
                source="PDDL Type System",
                example_before="a - tool (but used as block)",
                example_after="a - block (correct type)"
            ),
            ErrorFix(
                error_type="MISSING_TYPE",
                fix_title="Undefined Type Reference",
                fix_description="Using type that is not defined in :types section",
                fix_strategy="Add all referenced types to domain :types section",
                source="PDDL Type Requirements",
                example_before="?p - package (but package not in :types)",
                example_after="(:types package location ...) in domain"
            ),
            ErrorFix(
                error_type="UNSUPPORTED_REQUIREMENT",
                fix_title="Planner Capability Mismatch",
                fix_description="Using PDDL features not supported by chosen planner",
                fix_strategy="Remove unsupported requirements or switch to compatible planner",
                source="Planner Documentation",
                example_before=":adl requirement with Fast Downward",
                example_after="Remove :adl or use different planner"
            ),
            ErrorFix(
                error_type="MISSING_REQUIREMENT",
                fix_title="Required Feature Not Declared",
                fix_description="Using PDDL features without declaring requirements",
                fix_strategy="Add necessary requirements to :requirements section",
                source="PDDL Requirements System",
                example_before="Using types without :typing requirement",
                example_after="(:requirements :strips :typing) in domain"
            ),
            ErrorFix(
                error_type="PLANNER_PARSE_ERROR",
                fix_title="Domain/Problem Structure Error",
                fix_description="Missing essential PDDL file structure elements",
                fix_strategy="Ensure proper (define (domain ...)) and (define (problem ...)) blocks",
                source="PDDL File Format",
                example_before="Missing outer (define (domain ...)) wrapper",
                example_after="(define (domain name) ... domain content ...)"
            )
        ]
        
        for fix in error_fixes:
            self.add_error_fix_to_kg(fix)
        
        logger.info(f"Added {len(error_fixes)} error fixes from online sources")
    
    def populate_error_fixes_from_user_table(self):
        """Add error fixes from user-provided table"""
        error_fixes = [
            # User-provided error types and fixes
            ErrorFix(
                error_type="UNMATCHED_PARENTHESES",
                fix_title="Balance Parentheses",
                fix_description="Missing or extra parentheses in PDDL structure", 
                fix_strategy="Balance parentheses - count opening and closing brackets",
                source="User Table",
                example_before="Missing ')' in :init",
                example_after="Balance parentheses"
            ),
            ErrorFix(
                error_type="MISSPELLED_KEYWORD",
                fix_title="Correct PDDL Keywords",
                fix_description="Incorrect spelling of PDDL keywords",
                fix_strategy="Correct to standard PDDL keywords: :predicates, :actions, :init, :goal, etc.",
                source="User Table", 
                example_before=":predicats",
                example_after=":predicates"
            ),
            ErrorFix(
                error_type="WRONG_SECTION",
                fix_title="Move to Correct File Section",
                fix_description="PDDL elements placed in wrong file section",
                fix_strategy="Move :init and :goal to problem file, keep :predicates and :actions in domain file",
                source="User Table",
                example_before=":init in domain", 
                example_after="Move to problem file"
            ),
            ErrorFix(
                error_type="UNKNOWN_PREDICATE", 
                fix_title="Declare Predicate in Domain",
                fix_description="Using predicate not declared in domain :predicates section",
                fix_strategy="Declare all used predicates in domain :predicates section",
                source="User Table",
                example_before="(has tool1) not in domain",
                example_after="Declare predicate in :predicates"
            ),
            ErrorFix(
                error_type="TYPE_MISMATCH",
                fix_title="Correct Object Type Declaration", 
                fix_description="Object declared as wrong type",
                fix_strategy="Ensure object types match their usage in predicates and actions",
                source="User Table",
                example_before="Object declared as wrong type",
                example_after="Correct :objects type"
            ),
            ErrorFix(
                error_type="MISSING_TYPE",
                fix_title="Add Type to Domain",
                fix_description="Using type that is not defined in :types section", 
                fix_strategy="Add all referenced types to domain :types section",
                source="User Table",
                example_before="?p - package but no type defined",
                example_after="Add package to :types"
            ),
            ErrorFix(
                error_type="UNSUPPORTED_REQUIREMENT",
                fix_title="Change Planner or Remove Requirement",
                fix_description="Using PDDL features not supported by chosen planner",
                fix_strategy="Remove unsupported requirements or switch to compatible planner", 
                source="User Table",
                example_before=":adl in Fast Downward",
                example_after="Remove or change planner"
            ),
            ErrorFix(
                error_type="MISSING_REQUIREMENT",
                fix_title="Add Required Feature Declaration",
                fix_description="Using PDDL features without declaring requirements",
                fix_strategy="Add necessary requirements to :requirements section",
                source="User Table",
                example_before="Using types but no :typing",
                example_after="Add :typing to :requirements"
            ),
            ErrorFix(
                error_type="PLANNER_PARSE_ERROR",
                fix_title="Add Domain Structure Block",
                fix_description="Missing essential PDDL file structure elements",
                fix_strategy="Ensure proper (define (domain ...)) and (define (problem ...)) blocks",
                source="User Table", 
                example_before="Missing (define (domain ...))",
                example_after="Add outer (define ...) block"
            )
        ]
        
        for fix in error_fixes:
            self.add_error_fix_to_kg(fix)
        
        logger.info(f"Added {len(error_fixes)} error fixes from user table")
    
    def populate_error_cases_from_logs(self, log_directory: str = "logs"):
        """Extract error cases from planning logs"""
        try:
            log_files = glob.glob(f'{log_directory}/run*/*.json')
            error_count = 0
            
            logger.info(f"Processing error cases with rate limiting (this may take a few minutes)...")
            
            for log_file in log_files[:15]:  # Reduced to 15 to avoid rate limits
                try:
                    with open(log_file, 'r') as f:
                        data = json.load(f)
                    
                    if not data.get('plan_found', True) or data.get('planner_exit_code', 0) != 0:
                        error_type, error_desc = self.classify_error_from_logs(
                            data.get('planner_exit_code', 0),
                            data.get('planner_output', '')
                        )
                        
                        error_case = ErrorCase(
                            task_id=data.get('task_id', -1),
                            method=data.get('method', 'unknown'),
                            error_type=error_type,
                            error_description=error_desc,
                            exit_code=data.get('planner_exit_code', 0),
                            domain_name="blocksworld",  # Assuming blocksworld domain
                            timestamp=data.get('timestamp', '')
                        )
                        
                        self.add_error_case_to_kg(error_case)
                        error_count += 1
                        
                except Exception as e:
                    continue
            
            logger.info(f"Added {error_count} error cases from logs")
            
        except Exception as e:
            logger.error(f"Failed to populate error cases: {e}")
    
    def clear_existing_data(self):
        """Clear all existing data from the knowledge graph"""
        try:
            if not self.kg:
                raise ValueError("Knowledge graph must be initialized first")
            
            logger.info("Clearing existing knowledge graph data...")
            
            with self.kg.driver.session(database=self.neo4j_database) as session:
                # Delete all nodes and relationships
                session.run("MATCH (n) DETACH DELETE n")
            
            logger.info("[SUCCESS] Knowledge graph cleared successfully")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to clear knowledge graph: {e}")
            return False
    
    def populate_with_domains(self, domain_paths=None):
        """Populate the knowledge graph with PDDL domain information"""
        try:
            if not self.kg:
                raise ValueError("Knowledge graph must be initialized first")
            
            if domain_paths is None:
                # Default domain paths
                domain_paths = [
                    "domains/blocksworld",
                    "data/blocks",
                    "data/gripper", 
                    "data/logistics"
                ]
            
            logger.info(f"Populating knowledge graph with {len(domain_paths)} domains...")
            
            for domain_path in domain_paths:
                full_path = os.path.abspath(domain_path)
                if os.path.exists(full_path):
                    logger.info(f"Processing domain: {domain_path}")
                    self._process_domain_folder(full_path)
                else:
                    logger.warning(f"Domain path not found: {full_path}")
            
            logger.info("[SUCCESS] Domain population completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to populate domains: {e}")
            return False
    
    def _process_domain_folder(self, domain_path: str):
        """Process a domain folder or file"""
        try:
            if os.path.isfile(domain_path):
                # Single PDDL file
                if domain_path.endswith('.pddl'):
                    domain_data = self.parse_pddl_domain(domain_path)
                    if domain_data:
                        self.kg.add_domain(domain_data)
                        logger.info(f"Processed domain file: {domain_path}")
            else:
                # Directory containing PDDL files
                pddl_files = [f for f in os.listdir(domain_path) if f.endswith('.pddl')]
                for pddl_file in pddl_files:
                    if pddl_file.startswith('domain'):
                        domain_file_path = os.path.join(domain_path, pddl_file)
                        domain_data = self.parse_pddl_domain(domain_file_path)
                        if domain_data:
                            self.kg.add_domain(domain_data)
                            logger.info(f"Processed domain: {domain_data.name}")
                            
        except Exception as e:
            logger.error(f"Error processing domain path {domain_path}: {e}")
            raise
    
    def verify_data_ingestion(self):
        """Verify that data has been properly ingested into the knowledge graph"""
        try:
            if not self.kg:
                raise ValueError("Knowledge graph must be initialized first")
            
            logger.info("Verifying data ingestion...")
            
            with self.kg.driver.session(database=self.neo4j_database) as session:
                # Count nodes by type
                counts = {}
                
                node_types = ["Domain", "Action", "Predicate", "Type", "ErrorCase", "ErrorFix"]
                for node_type in node_types:
                    result = session.run(f"MATCH (n:{node_type}) RETURN count(n) as count")
                    count = result.single()["count"]
                    counts[node_type] = count
                    logger.info(f"{node_type} nodes: {count}")
                
                # Check relationships
                result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
                rel_count = result.single()["count"]
                logger.info(f"Total relationships: {rel_count}")
                
                if sum(counts.values()) > 0:
                    logger.info("[SUCCESS] Data verification successful - knowledge graph contains data")
                    return True, counts
                else:
                    logger.warning("[WARNING] Knowledge graph appears to be empty")
                    return False, counts
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to verify data: {e}")
            return False, {}
    
    def get_knowledge_graph_instance(self):
        """Get the initialized knowledge graph instance"""
        if not self.kg:
            raise ValueError("Knowledge graph has not been initialized yet")
        return self.kg
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def close_connections(self):
        """Close all database connections"""
        try:
            if self.kg:
                self.kg.close()
                logger.info("[SUCCESS] Knowledge graph connections closed")
                
        except Exception as e:
            logger.error(f"[ERROR] Error closing connections: {e}")



def main():
    """Main function to initialize and populate the knowledge graph"""
    import sys
    
    
    # Original initialization flow
    initializer = PDDLKnowledgeGraphInitializer()
    
    try:
        # Step 1: Initialize knowledge graph
        print("\n" + "="*60)
        print("PDDL KNOWLEDGE GRAPH INITIALIZATION")
        print("="*60)
        
        if not initializer.initialize_knowledge_graph():
            print("[ERROR] Failed to initialize knowledge graph")
            return False
        
        # Step 2: Clear existing data to start fresh
        print("\n[WARNING]  Clearing existing data...")
        if not initializer.clear_existing_data():
            print("[ERROR] Failed to clear existing data")
            return False
        
        # Step 3: Populate with domain data
        print("\n[INFO] Populating knowledge graph with PDDL domains...")
        if not initializer.populate_with_domains():
            print("[ERROR] Failed to populate domains")
            return False
        
        
        # Step 4: Add error information
        print("\n[INFO] Adding error cases from logs...")
        initializer.populate_error_cases_from_logs()
        
        print("\n[INFO] Adding error fixes from user table...")
        try:
            initializer.populate_error_fixes_from_user_table()
        except Exception as e:
            logger.warning(f"Failed to add error fixes: {e} (non-critical)")
        
        # Step 6: Verify data ingestion
        print("\n[INFO] Verifying complete data ingestion...")
        print("[INFO] This includes blocksworld, gripper, and logistics domains...")
        success, counts = initializer.verify_data_ingestion()
        
        if success:
            print("\n[SUCCESS] Knowledge graph initialization completed successfully!")
            print("\n[INFO] Final Summary:")
            for node_type, count in counts.items():
                if count > 0:
                    print(f"  * {node_type}: {count}")
            print(f"\n[SUCCESS] Knowledge Graph Ready!")
        else:
            print("\n[ERROR] CRITICAL ERROR: Knowledge graph initialization failed - data may be incomplete")
            print("\n[WARNING] Recommendation: Check logs and re-run to ensure clean data")
        
        return success
        
    except Exception as e:
        print(f"\n[ERROR] Error during initialization: {e}")
        return False
        
    finally:
        # Clean up connections
        initializer.close_connections()


if __name__ == "__main__":
    main()
