"""
Improved PDDL Parser for Domain and Problem Files
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import pddlpy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PDDLDomain:
    """Represents a PDDL domain"""
    name: str
    types: List[str]
    predicates: Dict[str, Any]
    actions: Dict[str, Any]
    description: str
    file_path: str

@dataclass
class PDDLAction:
    """Represents a PDDL action"""
    name: str
    parameters: List[str]
    preconditions: List[str]
    effects: List[str]
    description: str
    domain_name: str

@dataclass
class PDDLPredicate:
    """Represents a PDDL predicate"""
    name: str
    parameters: List[str]
    description: str
    domain_name: str

class ImprovedPDDLParser:
    """Improved parser for PDDL domains and problems"""
    
    def __init__(self):
        self.parsed_domains = {}
        self.parsed_problems = {}
        
    def parse_domain_directory(self, data_directory: str) -> Dict[str, Any]:
        """Parse all domain+problem pairs in subdirectories"""
        results = {
            'domains': [],
            'actions': [],
            'predicates': [],
            'types': [],
            'parsing_errors': []
        }
        
        data_path = Path(data_directory)
        if not data_path.exists():
            logger.error(f"Data directory not found: {data_directory}")
            return results
            
        # Process each subdirectory
        for subdir in data_path.iterdir():
            if subdir.is_dir():
                domain_file = subdir / "domain.pddl"
                problem_file = subdir / "p_example.pddl"
                
                if domain_file.exists() and problem_file.exists():
                    try:
                        domain_data = self.parse_domain_with_problem(
                            str(domain_file), str(problem_file)
                        )
                        if domain_data:
                            results['domains'].append(domain_data['domain'])
                            results['actions'].extend(domain_data['actions'])
                            results['predicates'].extend(domain_data['predicates'])
                            results['types'].extend(domain_data['types'])
                            
                    except Exception as e:
                        error_msg = f"Failed to parse {subdir.name}: {str(e)}"
                        logger.error(error_msg)
                        results['parsing_errors'].append(error_msg)
                else:
                    logger.warning(f"Missing files in {subdir.name}")
                    
        logger.info(f"Parsed {len(results['domains'])} domains, "
                   f"{len(results['actions'])} actions, "
                   f"{len(results['predicates'])} predicates")
        
        return results
    
    def parse_domain_with_problem(self, domain_file: str, problem_file: str) -> Optional[Dict[str, Any]]:
        """Parse a domain file with its corresponding problem file"""
        try:
            # Use pddlpy to parse both files
            parser = pddlpy.DomainProblem(domain_file, problem_file)
            domain_name = parser.domain.name
            
            logger.info(f"Parsing domain: {domain_name}")
            
            # Extract domain information
            domain_data = PDDLDomain(
                name=domain_name,
                types=self._extract_types(parser),
                predicates=self._extract_predicates_dict(parser),
                actions=self._extract_actions_dict(parser),
                description=self._generate_domain_description(parser, domain_name),
                file_path=domain_file
            )
            
            # Extract detailed actions
            actions = []
            for action_name, action_obj in parser.domain.operators.items():
                action = PDDLAction(
                    name=action_name,
                    parameters=self._extract_action_parameters(action_obj),
                    preconditions=self._extract_action_preconditions(action_obj),
                    effects=self._extract_action_effects(action_obj),
                    description=self._generate_action_description(action_name, action_obj),
                    domain_name=domain_name
                )
                actions.append(action)
            
            # Extract detailed predicates
            predicates = []
            for pred_name, pred_obj in parser.domain.predicates.items():
                predicate = PDDLPredicate(
                    name=pred_name,
                    parameters=self._extract_predicate_parameters(pred_obj),
                    description=self._generate_predicate_description(pred_name, pred_obj),
                    domain_name=domain_name
                )
                predicates.append(predicate)
            
            # Extract types
            types_list = []
            if hasattr(parser.domain, 'types') and parser.domain.types:
                for type_name in parser.domain.types:
                    types_list.append({
                        'name': type_name,
                        'domain_name': domain_name,
                        'description': f"Type {type_name} in {domain_name} domain"
                    })
            
            return {
                'domain': domain_data,
                'actions': actions,
                'predicates': predicates,
                'types': types_list
            }
            
        except Exception as e:
            logger.error(f"Error parsing {domain_file}: {e}")
            return None
    
    def _extract_types(self, parser) -> List[str]:
        """Extract types from domain"""
        types = []
        if hasattr(parser.domain, 'types') and parser.domain.types:
            types = list(parser.domain.types.keys()) if isinstance(parser.domain.types, dict) else list(parser.domain.types)
        return types
    
    def _extract_predicates_dict(self, parser) -> Dict[str, Any]:
        """Extract predicates as dictionary"""
        predicates = {}
        if hasattr(parser.domain, 'predicates'):
            for pred_name, pred_obj in parser.domain.predicates.items():
                predicates[pred_name] = {
                    'parameters': self._extract_predicate_parameters(pred_obj),
                    'arity': len(self._extract_predicate_parameters(pred_obj))
                }
        return predicates
    
    def _extract_actions_dict(self, parser) -> Dict[str, Any]:
        """Extract actions as dictionary"""
        actions = {}
        if hasattr(parser.domain, 'operators'):
            for action_name, action_obj in parser.domain.operators.items():
                actions[action_name] = {
                    'parameters': self._extract_action_parameters(action_obj),
                    'preconditions': self._extract_action_preconditions(action_obj),
                    'effects': self._extract_action_effects(action_obj)
                }
        return actions
    
    def _extract_action_parameters(self, action_obj) -> List[str]:
        """Extract parameters from action"""
        params = []
        if hasattr(action_obj, 'variable_list'):
            for var, var_type in action_obj.variable_list.items():
                params.append(f"{var} - {var_type}")
        return params
    
    def _extract_action_preconditions(self, action_obj) -> List[str]:
        """Extract preconditions from action"""
        preconditions = []
        if hasattr(action_obj, 'precondition_pos'):
            for precond in action_obj.precondition_pos:
                preconditions.append(str(precond))
        if hasattr(action_obj, 'precondition_neg'):
            for precond in action_obj.precondition_neg:
                preconditions.append(f"(not {precond})")
        return preconditions
    
    def _extract_action_effects(self, action_obj) -> List[str]:
        """Extract effects from action"""
        effects = []
        if hasattr(action_obj, 'effect_pos'):
            for effect in action_obj.effect_pos:
                effects.append(str(effect))
        if hasattr(action_obj, 'effect_neg'):
            for effect in action_obj.effect_neg:
                effects.append(f"(not {effect})")
        return effects
    
    def _extract_predicate_parameters(self, pred_obj) -> List[str]:
        """Extract parameters from predicate"""
        params = []
        if hasattr(pred_obj, 'variable_list'):
            for var, var_type in pred_obj.variable_list.items():
                params.append(f"{var} - {var_type}")
        elif hasattr(pred_obj, 'signature'):
            # Handle different predicate representations
            params = [str(p) for p in pred_obj.signature]
        return params
    
    def _generate_domain_description(self, parser, domain_name: str) -> str:
        """Generate natural language description of domain"""
        num_actions = len(parser.domain.operators) if hasattr(parser.domain, 'operators') else 0
        num_predicates = len(parser.domain.predicates) if hasattr(parser.domain, 'predicates') else 0
        num_types = len(parser.domain.types) if hasattr(parser.domain, 'types') else 0
        
        description = f"The {domain_name} domain contains {num_actions} actions, {num_predicates} predicates, and {num_types} types. "
        
        # Add domain-specific descriptions
        if 'blocks' in domain_name.lower():
            description += "This is a classic blocks world domain for stacking and unstacking blocks."
        elif 'gripper' in domain_name.lower():
            description += "This is a gripper domain involving robots picking up and moving objects with grippers."
        elif 'logistics' in domain_name.lower():
            description += "This is a logistics domain for transportation planning with trucks, packages, and locations."
        
        return description
    
    def _generate_action_description(self, action_name: str, action_obj) -> str:
        """Generate natural language description of action"""
        num_params = len(self._extract_action_parameters(action_obj))
        num_preconds = len(self._extract_action_preconditions(action_obj))
        num_effects = len(self._extract_action_effects(action_obj))
        
        description = f"The {action_name} action takes {num_params} parameters, has {num_preconds} preconditions, and {num_effects} effects. "
        
        # Add action-specific descriptions
        action_descriptions = {
            'pickup': 'Used to pick up objects from surfaces.',
            'putdown': 'Used to put down held objects onto surfaces.',
            'stack': 'Used to place one block on top of another.',
            'unstack': 'Used to remove a block from the top of another block.',
            'move': 'Used to transport objects or agents between locations.',
            'load-truck': 'Used to load packages into trucks for transportation.',
            'unload-truck': 'Used to unload packages from trucks.',
            'drive-truck': 'Used to move trucks between different locations.',
            'fly-airplane': 'Used to move airplanes between different cities.'
        }
        
        if action_name in action_descriptions:
            description += action_descriptions[action_name]
        
        return description
    
    def _generate_predicate_description(self, pred_name: str, pred_obj) -> str:
        """Generate natural language description of predicate"""
        num_params = len(self._extract_predicate_parameters(pred_obj))
        description = f"The {pred_name} predicate takes {num_params} parameters. "
        
        # Add predicate-specific descriptions
        predicate_descriptions = {
            'at': 'Indicates the location or position of an object.',
            'on': 'Indicates that one object is on top of another.',
            'clear': 'Indicates that the top of an object is clear/empty.',
            'holding': 'Indicates that an agent is holding an object.',
            'handempty': 'Indicates that an agent\'s hand is empty.',
            'ontable': 'Indicates that an object is directly on the table.',
            'in': 'Indicates containment relationship between objects.',
            'free': 'Indicates that a gripper or hand is free/available.'
        }
        
        if pred_name in predicate_descriptions:
            description += predicate_descriptions[pred_name]
        
        return description
