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

class AlfworldTask(NamedTuple):
    task_id: str
    trial_id: str
    task_type: str
    target_object: str
    toggle_target: str
    description: str
    scene_num: int
    floor_plan: str

class AlfworldInitialState(NamedTuple):
    trial_id: str
    predicates: List[str]
    objects: List[str]
    locations: List[str]
    receptacles: List[str]

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
            "alfred": "ALFWORLD domain for household tasks involving object manipulation, navigation, and interaction with appliances"
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
                
                node_types = ["Domain", "Action", "Predicate", "Type", "Task", "InitialState", "ErrorCase", "ErrorFix"]
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
    
    def parse_alfworld_traj_data(self, traj_file_path: str) -> Dict[str, Any]:
        """Parse ALFWORLD trajectory data JSON file"""
        try:
            with open(traj_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.error(f"Error parsing trajectory file {traj_file_path}: {e}")
            return None
    
    def parse_alfworld_initial_state(self, pddl_file_path: str) -> AlfworldInitialState:
        """Parse ALFWORLD initial state PDDL file"""
        try:
            with open(pddl_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract trial ID from problem name
            trial_match = re.search(r'plan_(trial_\w+)', content)
            trial_id = trial_match.group(1) if trial_match else "unknown_trial"
            
            # Extract objects
            objects = []
            objects_section = re.search(r':objects\s+(.*?)\s*\)', content, re.DOTALL)
            if objects_section:
                obj_lines = objects_section.group(1).strip().split('\n')
                for line in obj_lines:
                    line = line.strip()
                    if line and not line.startswith(';'):
                        # Extract object names before '-' type declaration
                        parts = line.split('-')
                        if len(parts) >= 2:
                            obj_names = parts[0].strip().split()
                            objects.extend(obj_names)
            
            # Extract predicates from :init section
            predicates = []
            init_section = re.search(r':init\s*\((.*?)\)\s*:goal', content, re.DOTALL)
            if init_section:
                init_content = init_section.group(1)
                pred_matches = re.findall(r'\([^)]+\)', init_content)
                predicates = [match.strip() for match in pred_matches]
            
            # Extract locations and receptacles from predicates
            locations = []
            receptacles = []
            for pred in predicates:
                if 'atLocation' in pred or 'location' in pred.lower():
                    parts = pred.split()
                    for part in parts:
                        if 'loc_' in part:
                            locations.append(part)
                elif 'receptacle' in pred.lower():
                    parts = pred.split()
                    for part in parts:
                        if '_bar_' in part and ('Drawer' in part or 'Desk' in part or 'Bed' in part):
                            receptacles.append(part)
            
            return AlfworldInitialState(
                trial_id=trial_id,
                predicates=predicates,
                objects=list(set(objects)),
                locations=list(set(locations)),
                receptacles=list(set(receptacles))
            )
            
        except Exception as e:
            logger.error(f"Error parsing initial state file {pddl_file_path}: {e}")
            return None
    
    def populate_alfworld_data(self, alfworld_data_path: str = r"C:\Users\manch\.cache\alfworld\json_2.1.1\train"):
        """Populate knowledge graph with ALFWORLD data"""
        try:
            if not self.kg:
                raise ValueError("Knowledge graph must be initialized first")
            
            if not os.path.exists(alfworld_data_path):
                logger.warning(f"ALFWORLD data path not found: {alfworld_data_path}")
                return False
            
            logger.info(f"Populating knowledge graph with ALL ALFWORLD data from: {alfworld_data_path}")
            
            # Process ALL task folders (~2400 training examples)
            task_folders = [d for d in os.listdir(alfworld_data_path) if os.path.isdir(os.path.join(alfworld_data_path, d))]
            logger.info(f"Found {len(task_folders)} task folders to process...")
            
            task_count = 0
            state_count = 0
            error_count = 0
            
            logger.info(f"Starting batch processing of {len(task_folders)} task folders...")
            
            for i, task_folder in enumerate(task_folders):
                try:
                    task_path = os.path.join(alfworld_data_path, task_folder)
                    
                    # Parse task info from folder name
                    task_parts = task_folder.split('-')
                    if len(task_parts) >= 4:
                        task_type = task_parts[0]
                        target_object = task_parts[1] if task_parts[1] != 'None' else None
                        toggle_target = task_parts[3] if len(task_parts) > 3 and task_parts[3] != 'None' else None
                        scene_num = int(task_parts[-1]) if task_parts[-1].isdigit() else 0
                    
                        # Process trial folders within this task
                        trial_folders = [d for d in os.listdir(task_path) if os.path.isdir(os.path.join(task_path, d))]
                    
                        for trial_folder in trial_folders:
                            trial_path = os.path.join(task_path, trial_folder)
                        
                            # Look for traj_data.json and initial_state.pddl
                            traj_file = os.path.join(trial_path, 'traj_data.json')
                            initial_state_file = os.path.join(trial_path, 'initial_state.pddl')
                        
                            if os.path.exists(traj_file) and os.path.exists(initial_state_file):
                                # Parse trajectory data
                                traj_data = self.parse_alfworld_traj_data(traj_file)
                            
                                if traj_data:
                                    # Create task description
                                    task_desc_parts = []
                                    if 'turk_annotations' in traj_data and 'anns' in traj_data['turk_annotations']:
                                        anns = traj_data['turk_annotations']['anns']
                                        if anns and len(anns) > 0 and 'task_desc' in anns[0]:
                                            task_desc_parts.append(anns[0]['task_desc'])
                                
                                    task_description = ' '.join(task_desc_parts) or f"{task_type} task with {target_object or 'object'}"
                                
                                    # Add task to knowledge graph
                                    task_data = {
                                        'task_id': task_folder,
                                        'trial_id': trial_folder,
                                        'task_type': task_type,
                                        'target_object': target_object or 'unknown',
                                        'toggle_target': toggle_target or 'none',
                                        'description': task_description,
                                        'scene_num': scene_num,
                                        'floor_plan': traj_data.get('scene', {}).get('floor_plan', 'unknown')
                                    }
                                
                                    try:
                                        self.kg.add_task(task_data)
                                        task_count += 1
                                        
                                        # Parse and add initial state
                                        initial_state = self.parse_alfworld_initial_state(initial_state_file)
                                        if initial_state:
                                            initial_state_data = {
                                                'trial_id': trial_folder,
                                                'predicates': initial_state.predicates,
                                                'objects': initial_state.objects,
                                                'locations': initial_state.locations,
                                                'receptacles': initial_state.receptacles
                                            }
                                            
                                            self.kg.add_initial_state(initial_state_data)
                                            state_count += 1
                                            
                                    except Exception as e:
                                        logger.error(f"Error adding task/state for {task_folder}/{trial_folder}: {e}")
                                        error_count += 1
                                        # Continue to next trial without break
                                
                                    # Progress logging
                                    if task_count % 100 == 0:
                                        logger.info(f"Progress: {task_count}/{len(task_folders)} tasks processed ({(i+1)/len(task_folders)*100:.1f}%)")
                                    
                                    # Minimal delay for large dataset
                                    if task_count % 10 == 0:
                                        time.sleep(0.01)
                                    
                except Exception as e:
                    error_count += 1
                    if error_count <= 5:  # Log first 5 errors
                        logger.error(f"Error processing task folder {task_folder}: {e}")
                    continue
            
            logger.info(f"[SUCCESS] Added {task_count} ALFWORLD tasks and {state_count} initial states from {len(task_folders)} task folders")
            if error_count > 0:
                logger.warning(f"[WARNING]  {error_count} task folders had processing errors")
            logger.info(f"[INFO] Processing complete - Full ALFWORLD dataset ingested ({task_count} tasks total)")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to populate ALFWORLD data: {e}")
            return False
    
    def generate_initial_state_from_traj(self, traj_data_path: str, domain_path: str, output_path: str = None) -> str:
        """Generate initial_state.pddl from traj_data.json and alfred.pddl"""
        try:
            # Parse trajectory data
            traj_data = self.parse_alfworld_traj_data(traj_data_path)
            if not traj_data:
                raise ValueError("Could not parse trajectory data")
            
            # Read domain file to get object types and predicates
            with open(domain_path, 'r', encoding='utf-8') as f:
                domain_content = f.read()
            
            # Extract task information
            task_id = traj_data.get('task_id', 'unknown_task')
            task_type = traj_data.get('task_type', 'unknown_type')
            scene_info = traj_data.get('scene', {})
            pddl_params = traj_data.get('pddl_params', {})
            
            # Query KG for similar tasks to get patterns
            similar_states = self._find_similar_initial_states(task_type, pddl_params)
            
            # Generate initial state content
            initial_state_content = self._build_initial_state_pddl(
                task_id, traj_data, domain_content, similar_states
            )
            
            # Write to file if output path specified
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(initial_state_content)
                logger.info(f"[SUCCESS] Generated initial state file: {output_path}")
            
            return initial_state_content
            
        except Exception as e:
            logger.error(f"[ERROR] Error generating initial state: {e}")
            raise
    
    def _find_similar_initial_states(self, task_type: str, pddl_params: Dict) -> List[Dict]:
        """Find similar initial states from the knowledge graph"""
        try:
            if not self.kg:
                return []
            
            # Create search query
            target_obj = pddl_params.get('object_target', '')
            toggle_obj = pddl_params.get('toggle_target', '')
            
            query_text = f"{task_type} {target_obj} {toggle_obj}"
            
            # Search for similar tasks
            similar_results = self.kg.similarity_search(query_text, limit=5)
            
            # Extract initial states from similar tasks
            similar_states = []
            with self.kg.driver.session() as session:
                for result in similar_results:
                    if result.get('labels', [''])[0] == 'Task':
                        task_name = result['node'].get('name', '')
                        # Find initial states for this task
                        state_result = session.run("""
                            MATCH (t:Task)-[:HAS_INITIAL_STATE]->(i:InitialState)
                            WHERE t.trial_id = $trial_id
                            RETURN i.predicates as predicates, i.objects as objects,
                                   i.locations as locations, i.receptacles as receptacles
                            LIMIT 1
                        """, {'trial_id': task_name})
                        
                        for record in state_result:
                            similar_states.append({
                                'predicates': record['predicates'],
                                'objects': record['objects'], 
                                'locations': record['locations'],
                                'receptacles': record['receptacles']
                            })
            
            return similar_states
            
        except Exception as e:
            logger.error(f"Error finding similar states: {e}")
            return []
    
    def _build_initial_state_pddl(self, task_id: str, traj_data: Dict, domain_content: str, similar_states: List[Dict]) -> str:
        """Build the complete initial state PDDL content"""
        try:
            scene_info = traj_data.get('scene', {})
            pddl_params = traj_data.get('pddl_params', {})
            object_poses = scene_info.get('object_poses', [])
            init_action = scene_info.get('init_action', {})
            
            # Extract object types from domain
            object_types = self._extract_object_types_from_domain(domain_content)
            receptacle_types = self._extract_receptacle_types_from_domain(domain_content)
            
            # Start building PDDL
            pddl_lines = []
            pddl_lines.append("")
            pddl_lines.append(f"(define (problem plan_{task_id})")
            pddl_lines.append("(:domain alfred)")
            pddl_lines.append("(:objects")
            pddl_lines.append("agent1 - agent")
            
            # Add all object types from domain
            for obj_type in sorted(object_types):
                pddl_lines.append(f"        {obj_type} - object")
            
            # Add all receptacle types  
            for recep_type in sorted(receptacle_types):
                pddl_lines.append(f"        {recep_type} - rtype")
            
            # Generate specific object instances and locations from scene
            object_instances, location_instances, receptacle_instances = self._generate_instances_from_scene(
                object_poses, similar_states
            )
            
            # Add specific instances
            for obj_instance in sorted(object_instances):
                pddl_lines.append(f"        {obj_instance} - object")
            
            for loc_instance in sorted(location_instances):
                pddl_lines.append(f"        {loc_instance} - location")
                
            for recep_instance in sorted(receptacle_instances):
                pddl_lines.append(f"        {recep_instance} - receptacle")
            
            pddl_lines.append(")")
            pddl_lines.append("    ")
            pddl_lines.append("")
            pddl_lines.append("(:init")
            pddl_lines.append("")
            
            # Generate init predicates
            init_predicates = self._generate_init_predicates(
                traj_data, object_instances, location_instances, receptacle_instances, similar_states
            )
            
            pddl_lines.extend(init_predicates)
            pddl_lines.append(")")
            pddl_lines.append("    ")
            
            # Generate goal from pddl_params
            goal_predicates = self._generate_goal_predicates(pddl_params)
            pddl_lines.append("")
            pddl_lines.append("        (:goal")
            pddl_lines.append("             (and")
            pddl_lines.extend(goal_predicates)
            pddl_lines.append("             )")
            pddl_lines.append("        )")
            pddl_lines.append("    )")
            pddl_lines.append("    ")
            
            return '\n'.join(pddl_lines)
            
        except Exception as e:
            logger.error(f"Error building PDDL: {e}")
            raise
    
    def _extract_object_types_from_domain(self, domain_content: str) -> List[str]:
        """Extract object types from domain file"""
        types = []
        # Look for object types in (:types section or from predicates
        basic_types = [
            'SaltShaker', 'HousePlant', 'Candle', 'SprayBottle', 'Bowl', 'Window', 'CD', 'Egg',
            'Glassbottle', 'Sink', 'Pillow', 'Spoon', 'SoapBottle', 'TeddyBear', 'ButterKnife',
            'Cup', 'Plate', 'RemoteControl', 'Tomato', 'Statue', 'HandTowel', 'Knife', 'StoveKnob',
            'LightSwitch', 'Pen', 'Painting', 'DishSponge', 'Vase', 'Mug', 'ToiletPaper', 'Box',
            'Mirror', 'Ladle', 'Fork', 'Blinds', 'Footstool', 'KeyChain', 'Cloth', 'Laptop',
            'TissueBox', 'PepperShaker', 'FloorLamp', 'WateringCan', 'Apple', 'Pan', 'PaperTowel',
            'PaperTowelRoll', 'Newspaper', 'Television', 'Chair', 'CellPhone', 'CreditCard',
            'Lettuce', 'BasketBall', 'Potato', 'Curtains', 'Boots', 'Pencil', 'AlarmClock',
            'ToiletPaperRoll', 'Spatula', 'Book', 'Bread', 'SoapBar', 'Watch', 'DeskLamp',
            'Kettle', 'Pot', 'ScrubBrush', 'WineBottle', 'ShowerDoor', 'Bathtub', 'LaundryHamperLid',
            'ShowerGlass', 'Poster', 'TennisRacket', 'BaseballBat', 'Towel', 'Plunger'
        ]
        
        # Add corresponding type names
        for obj_type in basic_types:
            types.append(f"{obj_type}Type - otype")
            
        return types
    
    def _extract_receptacle_types_from_domain(self, domain_content: str) -> List[str]:
        """Extract receptacle types from domain file"""
        return [
            'SafeType - rtype', 'DrawerType - rtype', 'CoffeeMachineType - rtype', 'HandTowelHolderType - rtype',
            'SinkBasinType - rtype', 'DresserType - rtype', 'LaundryHamperType - rtype', 'TVStandType - rtype',
            'BathtubBasinType - rtype', 'CabinetType - rtype', 'FridgeType - rtype', 'DeskType - rtype',
            'ToiletType - rtype', 'CartType - rtype', 'SideTableType - rtype', 'SofaType - rtype',
            'CoffeeTableType - rtype', 'DiningTableType - rtype', 'CounterTopType - rtype', 'GarbageCanType - rtype',
            'ArmChairType - rtype', 'ShelfType - rtype', 'MicrowaveType - rtype', 'ToasterType - rtype',
            'BedType - rtype', 'PaintingHangerType - rtype', 'TowelHolderType - rtype', 'ToiletPaperHangerType - rtype',
            'StoveBurnerType - rtype', 'OttomanType - rtype'
        ]
    
    def _generate_instances_from_scene(self, object_poses: List, similar_states: List[Dict]) -> tuple:
        """Generate specific object, location, and receptacle instances from scene data"""
        object_instances = set()
        location_instances = set()
        receptacle_instances = set()
        
        # Process object poses to create instances
        for pose in object_poses:
            obj_name = pose.get('objectName', '')
            if obj_name:
                # Convert Unity coordinates to PDDL location format
                pos = pose.get('position', {})
                x, y, z = pos.get('x', 0), pos.get('y', 0), pos.get('z', 0)
                
                # Create PDDL-style object name
                pddl_obj_name = self._unity_to_pddl_object_name(obj_name, x, y, z)
                object_instances.add(pddl_obj_name)
                
                # Create location based on coordinates
                location_name = self._coords_to_location(x, y, z)
                location_instances.add(location_name)
        
        # Add common receptacles from similar states
        for state in similar_states:
            if 'receptacles' in state:
                for recep in state['receptacles']:
                    receptacle_instances.add(recep)
            if 'locations' in state:
                for loc in state['locations']:
                    location_instances.add(loc)
        
        return list(object_instances), list(location_instances), list(receptacle_instances)
    
    def _unity_to_pddl_object_name(self, unity_name: str, x: float, y: float, z: float) -> str:
        """Convert Unity object name and coordinates to PDDL format"""
        # Extract base object type
        base_name = unity_name.split('_')[0] if '_' in unity_name else unity_name
        
        # Convert coordinates to PDDL format (like AlarmClock_bar__plus_01_dot_65_bar__plus_00_dot_80_bar__minus_01_dot_28)
        x_str = f"plus_{abs(x):.2f}".replace('.', '_dot_') if x >= 0 else f"minus_{abs(x):.2f}".replace('.', '_dot_')
        y_str = f"plus_{abs(y):.2f}".replace('.', '_dot_') if y >= 0 else f"minus_{abs(y):.2f}".replace('.', '_dot_')
        z_str = f"plus_{abs(z):.2f}".replace('.', '_dot_') if z >= 0 else f"minus_{abs(z):.2f}".replace('.', '_dot_')
        
        return f"{base_name}_bar__{x_str}_bar__{y_str}_bar__{z_str}"
    
    def _coords_to_location(self, x: float, y: float, z: float) -> str:
        """Convert coordinates to location format"""
        # Convert to grid-based location (similar to existing format)
        grid_x = int(round(x * 3))  # Scale and round
        grid_z = int(round(z * 3))  # Scale and round
        grid_y = int(round(y * 60)) if y > 0 else 30  # Default height
        
        return f"loc_bar_{grid_x}_bar_{grid_z}_bar_0_bar_{grid_y}"
    
    def _generate_init_predicates(self, traj_data: Dict, objects: List, locations: List, receptacles: List, similar_states: List[Dict]) -> List[str]:
        """Generate initialization predicates"""
        predicates = []
        scene_info = traj_data.get('scene', {})
        init_action = scene_info.get('init_action', {})
        object_poses = scene_info.get('object_poses', [])
        
        # Agent initial location
        agent_x = init_action.get('x', 0)
        agent_z = init_action.get('z', 0)
        agent_y = init_action.get('y', 0.9)
        agent_location = self._coords_to_location(agent_x, agent_y, agent_z)
        predicates.append(f"        (atLocation agent1 {agent_location})")
        predicates.append("        ")
        
        # Object type declarations and properties
        type_predicates = []
        property_predicates = []
        receptacle_predicates = []
        location_predicates = []
        containment_predicates = []
        
        for pose in object_poses:
            obj_name = pose.get('objectName', '')
            if obj_name:
                pos = pose.get('position', {})
                x, y, z = pos.get('x', 0), pos.get('y', 0), pos.get('z', 0)
                
                pddl_obj_name = self._unity_to_pddl_object_name(obj_name, x, y, z)
                obj_location = self._coords_to_location(x, y, z)
                base_type = obj_name.split('_')[0]
                
                # Object type
                type_predicates.append(f"        (objectType {pddl_obj_name} {base_type}Type)")
                
                # Object properties based on type
                if base_type in ['AlarmClock', 'Book', 'CD', 'CellPhone', 'CreditCard', 'KeyChain', 'Laptop', 'Mug', 'Pen', 'Pencil', 'Pillow', 'Watch']:
                    property_predicates.append(f"        (pickupable {pddl_obj_name})")
                
                if base_type in ['DeskLamp', 'FloorLamp']:
                    property_predicates.append(f"        (toggleable {pddl_obj_name})")
                
                if base_type in ['Mug', 'Bowl', 'Cup']:
                    property_predicates.append(f"        (cleanable {pddl_obj_name})")
                    property_predicates.append(f"        (heatable {pddl_obj_name})")
                    property_predicates.append(f"        (coolable {pddl_obj_name})")
                
                # Object location
                location_predicates.append(f"        (objectAtLocation {pddl_obj_name} {obj_location})")
        
        # Add receptacle and containment relationships from similar states
        for state in similar_states[:1]:  # Use first similar state as template
            if 'predicates' in state:
                for pred in state['predicates']:
                    if 'receptacleAtLocation' in pred or 'inReceptacle' in pred:
                        containment_predicates.append(f"        {pred}")
        
        # Combine all predicates
        predicates.extend(type_predicates)
        predicates.append("        ")
        predicates.extend(property_predicates)
        predicates.append("        ")
        predicates.extend(location_predicates)
        predicates.append("        ")
        predicates.extend(containment_predicates)
        
        return predicates
    
    def _generate_goal_predicates(self, pddl_params: Dict) -> List[str]:
        """Generate goal predicates based on task parameters"""
        goal_lines = []
        
        target_obj = pddl_params.get('object_target', '')
        toggle_obj = pddl_params.get('toggle_target', '')
        
        if toggle_obj:
            goal_lines.append("                 (exists (?ot - object")
            goal_lines.append("                          ?r - receptacle")
            goal_lines.append("                          ?a - agent")
            goal_lines.append("                          ?l - location)")
            goal_lines.append("                     (and")
            goal_lines.append(f"                         (objectType ?ot {toggle_obj}Type)")
            goal_lines.append("                         (toggleable ?ot)")
            goal_lines.append("                         (isToggled ?ot)")
            goal_lines.append("                         (receptacleAtLocation ?r ?l)")
            goal_lines.append("                         (atLocation ?a ?l)")
            goal_lines.append("                         (inReceptacle ?ot ?r)")
            goal_lines.append("                     )")
            goal_lines.append("                 )")
        
        if target_obj:
            goal_lines.append("                 (exists (?o - object")
            goal_lines.append("                          ?a - agent)")
            goal_lines.append("                     (and")
            goal_lines.append(f"                         (objectType ?o {target_obj}Type)")
            goal_lines.append("                         (holds ?a ?o)")
            goal_lines.append("                     )")
            goal_lines.append("                 )")
        
        return goal_lines
    
    def close_connections(self):
        """Close all database connections"""
        try:
            if self.kg:
                self.kg.close()
                logger.info("[SUCCESS] Knowledge graph connections closed")
                
        except Exception as e:
            logger.error(f"[ERROR] Error closing connections: {e}")


def generate_initial_state_standalone(traj_data_path: str, domain_path: str, output_path: str):
    """Standalone function to generate initial state for validation"""
    try:
        print(f"\n🔄 Generating initial state from trajectory data...")
        print(f"📂 Trajectory file: {traj_data_path}")
        print(f"📂 Domain file: {domain_path}")
        print(f"📂 Output file: {output_path}")
        
        initializer = PDDLKnowledgeGraphInitializer()
        
        # Generate initial state
        initial_state_content = initializer.generate_initial_state_from_traj(
            traj_data_path, domain_path, output_path
        )
        
        print(f"\n[SUCCESS] Successfully generated initial state file!")
        print(f"📄 Content preview (first 500 chars):")
        print("=" * 50)
        print(initial_state_content[:500] + "..." if len(initial_state_content) > 500 else initial_state_content)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error generating initial state: {e}")
        return False
    finally:
        if 'initializer' in locals():
            initializer.close_connections()

def main():
    """Main function to initialize and populate the knowledge graph"""
    import sys
    
    # Check if this is a validation call
    if len(sys.argv) == 4 and sys.argv[1] == "--generate-initial-state":
        traj_path = sys.argv[2]
        output_path = sys.argv[3]
        domain_path = "alfred.pddl"  # Default domain file
        
        return generate_initial_state_standalone(traj_path, domain_path, output_path)
    
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
        
        # Step 4: Add ALFWORLD data (all ~2400 examples)
        print("\n[INFO] Populating knowledge graph with FULL ALFWORLD dataset (~2400 examples)...")
        print("[INFO]  This may take several minutes to process all training examples...")
        if not initializer.populate_alfworld_data():
            print("[ERROR] Failed to populate ALFWORLD data")
            return False
        
        # Step 5: Add error information
        print("\n[INFO] Adding error cases from logs...")
        initializer.populate_error_cases_from_logs()
        
        print("\n[INFO] Adding error fixes from user table...")
        try:
            initializer.populate_error_fixes_from_user_table()
        except Exception as e:
            logger.warning(f"Failed to add error fixes: {e} (non-critical)")
        
        # Step 6: Verify data ingestion
        print("\n[INFO] Verifying complete data ingestion...")
        print("[INFO] This includes all domains + full ALFWORLD dataset...")
        success, counts = initializer.verify_data_ingestion()
        
        if success:
            print("\n[SUCCESS] Knowledge graph initialization completed successfully!")
            print("\n[INFO] Final Summary:")
            for node_type, count in counts.items():
                if count > 0:
                    print(f"  * {node_type}: {count}")
            print(f"\n[SUCCESS] Knowledge Graph Ready with Full Dataset!")
            print(f"  * Total ALFWORLD Training Examples: ~{counts.get('Task', 0)}")
            print(f"  * Total Initial States: ~{counts.get('InitialState', 0)}")
            print(f"  * Ready for initial_state.pddl generation!")
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
