# LLM+P code
This repo contains the source code for making plans based on problems decribed by natural language.

## Dependency

1. Install Cohere library. Put Cohere API key under the ```.env``` file.
2. Install fast-download.

## Running Code
To run a for a specific task in a specific domain using a specific method:
```
python main.py --domain DOMAIN --method METHOD --task TASK_ID
```
`DOMAIN` is selected from
```[blocksworld]```

`METHOD` is selected from
```[llm_ic_pddl_planner, llm_pddl_planner, llm_planner, llm_ic_planner]```

Alternatively, you can just use:

```
bash run.sh DOMAIN METHOD TASK_ID
```


## The File Hierarchy:
```
llm-pddl
 └─main.py                         (the main python script)
 └─.env                            (you should place your cohere key here)
 └─domains                         (the generated domain files)
    └─ blocksworld
        └─ description_geneator.py (generating natural language description)
        └─ p_example.nl            (example natural language)
        └─ p_example.pddl          (example problem pddl file)
        └─ domain.pddl             (the shared domain.pddl file for all problems)
        └─ xxx.nl                  (task natural language description)
        └─ xxx.pddl                (ground-truth problem pddl, might not be used)
 └─experiments
   └─problems                        (the generated problem pddl files)
      └─ llm                         (empty, since llm -> plan does not generate pddl)
      └─ llm_ic                      (empty, since llm + context -> plan does not generate pddl)    
      └─ llm_pddl                    (baseline 2: llm -> p.pddl)
      └─ llm_ic_pddl                 (ours: llm + context -> p.pddl)
         └─ blocksworld
   └─plans                           (the tmp folder for storing raw solutions found by fast-downward)
      └─ llm                         (empty, since llm -> plan does not generate raw plans)
      └─ llm_ic                      (empty, since llm + context -> plan does not generate raw plans)
      └─ llm_pddl                    (baseline 2: llm -> p.pddl)
      └─ llm_ic_pddl                 (ours: llm + context -> p.pddl)
         └─ blocksworld
   └─results                         (the final plan in natural language)
      └─ llm                         (baseline 1: llm -> plan)
      └─ llm_ic                      (baseline 3: llm + context -> plan)
      └─ llm_pddl                    (baseline 2: llm -> p.pddl)
      └─ llm_ic_pddl                 (ours: llm + context -> p.pddl)
         └─ blocksworld
 ```
