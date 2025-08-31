# LLM PDDL Framework

A research framework for evaluating Large Language Model performance on PDDL (Planning Domain Definition Language) planning problems using knowledge graphs and RAG (Retrieval-Augmented Generation) techniques.

## Overview

This framework implements multiple approaches for solving planning problems:

- **LLM-as-Planner**: Direct text-based planning
- **LLM-IC**: In-context learning with examples  
- **LLM-PDDL**: PDDL code generation
- **LLM-IC-PDDL**: PDDL generation with context
- **LLM-IC-PDDL-RAG**: Enhanced with knowledge graph RAG for error correction

## Project Structure

```
├── main.py                    # Main execution script
├── kg_initializer.py          # Knowledge graph initialization
├── knowledge_graph_qa.py      # Knowledge graph QA system
├── graph_rag_qa.py           # Graph RAG implementation
├── domains/                   # PDDL domain definitions
│   ├── blocksworld/          # Blocksworld domain and problems
│   └── grippers/             # Gripper domain and problems
├── data/                     # Additional domain data
│   ├── blocksworld/
│   ├── gripper/
├── experiments/              # Experiment results
└── logs/                     # Execution logs
```

## Setup

1. **Environment Variables**
   Create a `.env` file with:
   ```
   COHERE_API_KEY=your_cohere_api_key
   NEO4J_URI=neo4j://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password
   NEO4J_DATABASE=neo4j
   HUGGINGFACE_TOKEN=your_hf_token
   ```

2. **Dependencies**
   - Python 3.8+
   - Cohere API
   - Neo4j Database
   - Fast Downward Planner
   - Required Python packages (cohere, neo4j, python-dotenv, etc.)

## Usage

### Basic Planning
```bash
python main.py --method llm_ic_pddl_planner --task 0 --run 1
```

### RAG-Enhanced Planning
```bash
python main.py --method llm_ic_pddl_rag --task 0 --run 1
```

### Initialize Knowledge Graph
```bash
python kg_initializer.py
```

## Methods

- `llm_planner`: Direct LLM text planning
- `llm_ic_planner`: In-context text planning
- `llm_pddl_planner`: PDDL generation without context
- `llm_ic_pddl_planner`: PDDL generation with context
- `llm_ic_pddl_rag`: RAG-enhanced PDDL error correction

## Features

- **Knowledge Graph Integration**: Neo4j-based storage of domain knowledge and error patterns
- **Error Classification**: Automatic PDDL error detection and categorization
- **RAG-Based Correction**: Retrieval-augmented generation for fixing planning failures
- **Comprehensive Logging**: Detailed execution tracking and result analysis
- **Multiple Domains**: Support for blocksworld, grippers, and logistics domains

## Research Focus

This framework enables research on:
- LLM performance in symbolic planning
- Knowledge graph-enhanced reasoning
- Error correction through retrieval-augmented generation
- Comparative analysis of different planning approaches

## Output

Results are organized in `experiments/` with generated PDDL files, plans, and detailed logs for analysis and evaluation.