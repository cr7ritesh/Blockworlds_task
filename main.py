import argparse
import glob
import os
import time
import backoff
import subprocess
import json
from dotenv import load_dotenv

import cohere

load_dotenv()

# FAST_DOWNWARD_ALIAS = "lama"
# FAST_DOWNWARD_ALIAS = "seq-opt-fdss-1"
FAST_DOWNWARD_ALIAS = "seq-opt-lmcut"  # Default alias for Fast Downward planner

class Logger:
    """Logger class to capture and store logs for RAG documentation"""
    
    def __init__(self, log_dir, task_id, method_name):
        self.log_dir = log_dir
        self.task_id = task_id
        self.method_name = method_name
        
        # Create log directory
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize log data structure
        self.log_data = {
            "task_id": task_id,
            "method": method_name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "prompt": "",
            "llm_response": "",
            "generated_domain_pddl": "",
            "generated_problem_pddl": "",
            "planner_command": "",
            "planner_output": "",
            "planner_errors": "",
            "planner_exit_code": None,
            "execution_time": 0,
            "plan_found": False,
            "plan_cost": None,
            "best_plan": ""
        }
    
    def log_prompt(self, prompt):
        """Log the prompt sent to LLM"""
        self.log_data["prompt"] = prompt
        
    def log_llm_response(self, response):
        """Log the raw LLM response"""
        self.log_data["llm_response"] = response
        
    def log_generated_pddl(self, domain_pddl, problem_pddl):
        """Log the generated PDDL files"""
        self.log_data["generated_domain_pddl"] = domain_pddl
        self.log_data["generated_problem_pddl"] = problem_pddl
        
    def log_planner_execution(self, command, output, errors, exit_code):
        """Log planner command execution details"""
        self.log_data["planner_command"] = command
        self.log_data["planner_output"] = output
        self.log_data["planner_errors"] = errors
        self.log_data["planner_exit_code"] = exit_code
        
    def log_plan_result(self, plan_found, plan_cost=None, best_plan=""):
        """Log the final planning result"""
        self.log_data["plan_found"] = plan_found
        self.log_data["plan_cost"] = plan_cost
        self.log_data["best_plan"] = best_plan
        
    def log_execution_time(self, execution_time):
        """Log total execution time"""
        self.log_data["execution_time"] = execution_time
        
    def save_logs(self):
        """Save logs to a single JSON file"""
        # Create filename: task_<id>_<method>.json
        json_filename = f"task_{self.task_id}_{self.method_name}.json"
        json_file = os.path.join(self.log_dir, json_filename)
        
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.log_data, f, indent=2, ensure_ascii=False)
        
        print(f"[LOG] Logs saved to {json_file}")

def get_cost(x):
    splitted = x.split()
    counter = 0
    found = False
    cost = 1e5
    for i, xx in enumerate(splitted):
        if xx == "cost":
            counter = i
            found = True
            break
    if found:
        cost = float(splitted[counter+2])
    return cost

def run_command_with_timeout(command, timeout_seconds=200, capture_output=False):
    """Run a command with timeout and return exit code, optionally capture output"""
    try:
        if capture_output:
            result = subprocess.run(
                command,
                shell=True,
                timeout=timeout_seconds,
                capture_output=True,
                text=True
            )
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(
                command,
                shell=True,
                timeout=timeout_seconds,
                capture_output=False,
                text=True
            )
            return result.returncode, "", ""
    except subprocess.TimeoutExpired:
        error_msg = f"Command timed out after {timeout_seconds} seconds"
        print(error_msg)
        return -1, "", error_msg  # Timeout error code
    except Exception as e:
        error_msg = f"Command failed with error: {e}"
        print(error_msg)
        return -2, "", error_msg  # Other error code

class Blocksworld:
    def __init__(self):
        self.name = 'blocksworld'
        self.context = ("p_example.nl", "p_example.pddl", "p_example.sol")
        self.tasks = [] # should be list of tuples like (descritpion, ground_truth_pddl)

        self.grab_tasks()

    def grab_tasks(self):
        path = f"./domains/{self.name}"
        nls = []
        for fn in glob.glob(f"{path}/*.nl"):
            fn_ = os.path.basename(fn)
            if "domain" not in fn_ and "p_example" not in fn_:
                if os.path.exists(fn.replace("nl", "pddl")):
                    nls.append(fn_)
        sorted_nls = sorted(nls)
        self.tasks = [(nl, nl.replace("nl", "pddl")) for nl in sorted_nls]

    def __len__(self):return len(self.tasks)

    def get_task_suffix(self, i):
        _, pddl = self.tasks[i]
        return f"{self.name}/{pddl}"

    def get_task_file(self, i):
        nl, pddl = self.tasks[i]
        return f"./domains/{self.name}/{nl}", f"./domains/{self.name}/{pddl}"

    def get_task(self, i):
        nl_f, pddl_f = self.get_task_file(i)
        
        with open(nl_f, 'r') as f:nl = f.read()
        with open(pddl_f, 'r') as f:pddl = f.read()
        
        return nl.strip(), pddl.strip()

    def get_context(self):
        nl_f = f"./domains/{self.name}/{self.context[0]}"
        pddl_f = f"./domains/{self.name}/{self.context[1]}"
        sol_f = f"./domains/{self.name}/{self.context[2]}"
        
        with open(nl_f, 'r') as f:nl = f.read()
        with open(pddl_f, 'r') as f:pddl = f.read()
        with open(sol_f, 'r') as f:sol = f.read()
        
        return nl.strip(), pddl.strip(), sol.strip()

    def get_domain_pddl(self):
        domain_pddl_f = self.get_domain_pddl_file()
        
        with open(domain_pddl_f, 'r') as f:domain_pddl = f.read()
        
        return domain_pddl.strip()

    def get_domain_pddl_file(self):return f"./domains/blocksworld/domain.pddl"

    def get_domain_nl(self):
        domain_nl_f = self.get_domain_nl_file()
        try:
            with open(domain_nl_f, 'r') as f:
                domain_nl = f.read()
        except:
            domain_nl = "Nothing"
        return domain_nl.strip()

    def get_domain_nl_file(self):return f"./domains/blocksworld/domain.nl"

class Planner:
    def __init__(self):
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.client = cohere.Client(self.cohere_api_key)

    def create_llm_prompt(self, task_nl, domain_nl):
        # Baseline 1 (LLM-as-P): directly ask the LLM for plan
        prompt = f"{domain_nl} \n" + \
                 f"Now consider a planning problem. " + \
                 f"The problem description is: \n {task_nl} \n" + \
                 f"Can you provide an optimal plan, in the way of a " + \
                 f"sequence of behaviors, to solve the problem?"
        return prompt

    def create_llm_ic_prompt(self, task_nl, domain_nl, context):
        # Baseline 2 (LLM-as-P with context): directly ask the LLM for plan
        context_nl, _, context_sol = context
        prompt = f"{domain_nl} \n" + \
                 f"An example planning problem is: \n {context_nl} \n" + \
                 f"A plan for the example problem is: \n {context_sol} \n" + \
                 f"Now I have a new planning problem and its description is: \n {task_nl} \n" + \
                 f"Can you provide an optimal plan, in the way of a " + \
                 f"sequence of behaviors, to solve the problem?" + \
                 f"The domain name should be 'blocksworld-4ops'."
        return prompt

    def create_llm_pddl_prompt(self, task_nl, domain_nl):
        # Generate both domain and problem PDDL files
        prompt = f"{domain_nl} \n" + \
                 f"Now consider a planning problem. " + \
                 f"The problem description is: \n {task_nl} \n" + \
                 f"Provide me with BOTH the domain PDDL file AND the problem PDDL file that describes " + \
                 f"the planning problem. Format your response as follows:\n" + \
                 f"DOMAIN:\n[domain PDDL content]\n\n" + \
                 f"PROBLEM:\n[problem PDDL content]\n\n" + \
                 f"Make sure both files use consistent naming and types. Do not provide any other explanations."
        return prompt

    def create_llm_ic_pddl_prompt(self, task_nl, domain_pddl, context):
        # Generate both domain and problem PDDL files with context
        context_nl, context_pddl, _ = context
        prompt = f"I want you to solve planning problems. " + \
                 f"Here is the domain PDDL file: \n {domain_pddl} \n" + \
                 f"An example planning problem is: \n {context_nl} \n" + \
                 f"The problem PDDL file to this problem is: \n {context_pddl} \n" + \
                 f"Now I have a new planning problem and its description is: \n {task_nl} \n" + \
                 f"Provide me with BOTH a domain PDDL file AND a problem PDDL file that describes " + \
                 f"the new planning problem. Format your response as follows:\n" + \
                 f"DOMAIN:\n[domain PDDL content]\n\n" + \
                 f"PROBLEM:\n[problem PDDL content]\n\n" + \
                 f"Make sure both files use consistent naming and types. Do not provide any other explanations."
        return prompt

    def query(self, prompt_text):
        server_cnt = 0
        result_text = ""
        
        while server_cnt < 10:
            try:
                @backoff.on_exception(backoff.expo, Exception)
                def completions_with_backoff(**kwargs):
                    return self.client.chat(**kwargs)

                response = completions_with_backoff(
                    model="command-r-plus",  # or "command-r" for faster responses
                    message=prompt_text,
                    temperature=0.0,
                    max_tokens=2048,
                    p=1.0,  # equivalent to top_p
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                result_text = response.text
                break
            except Exception as e:
                server_cnt += 1
                print(f"Error: {e}")
                time.sleep(2 ** server_cnt)
        return result_text

    def parse_domain_problem_result(self, response):
        """Parse LLM response containing both domain and problem PDDL"""
        try:
            # Clean up markdown formatting
            response = self.clean_pddl_response(response)
            
            # Split response into domain and problem parts
            parts = response.split("PROBLEM:")
            if len(parts) != 2:
                # Try alternative format
                parts = response.split("DOMAIN:")
                if len(parts) == 2:
                    domain_part = parts[1].split("PROBLEM:")[0].strip()
                    problem_part = parts[1].split("PROBLEM:")[1].strip()
                else:
                    # Fallback: assume first PDDL block is domain, second is problem
                    pddl_blocks = response.split("(define")
                    if len(pddl_blocks) >= 3:
                        domain_pddl = "(define" + pddl_blocks[1]
                        problem_pddl = "(define" + pddl_blocks[2]
                        return domain_pddl.strip(), problem_pddl.strip()
                    else:
                        raise ValueError("Could not parse domain and problem from response")
            else:
                domain_part = parts[0].replace("DOMAIN:", "").strip()
                problem_part = parts[1].strip()
            
            # Clean up each part individually
            domain_part = self.clean_pddl_response(domain_part)
            problem_part = self.clean_pddl_response(problem_part)
            
            return domain_part, problem_part
        except Exception as e:
            print(f"Error parsing domain/problem response: {e}")
            # Fallback: return original response as problem, empty domain
            return "", response

    def clean_pddl_response(self, pddl_text):
        """Remove markdown formatting and clean up PDDL text"""
        # Remove markdown code blocks
        pddl_text = pddl_text.replace('```pddl', '').replace('```', '')
        
        # Remove extra whitespace
        pddl_text = pddl_text.strip()
        
        # Ensure it starts with (define if it's valid PDDL
        if pddl_text and not pddl_text.startswith('(define'):
            # Try to find the start of PDDL content
            define_index = pddl_text.find('(define')
            if define_index != -1:
                pddl_text = pddl_text[define_index:]
        
        return pddl_text

def llm_ic_pddl_planner(args, planner, domain):
    """
    Our method:
        context: (task natural language, task problem PDDL)
        Condition on the context (task description -> task problem PDDL),
        LLM will be asked to provide both domain and problem PDDL of a new task description.
        Then, we use a planner to find the near optimal solution, and translate
        that back to natural language.
    """
    context     = domain.get_context()
    domain_pddl = domain.get_domain_pddl()
    
    # Initialize logger
    log_dir = f"./logs/run{args.run}"
    logger = Logger(log_dir, args.task, "llm_ic_pddl")
    
    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm_ic_pddl/{domain.name}"
    plan_folder    = f"./experiments/run{args.run}/plans/llm_ic_pddl/{domain.name}"
    result_folder  = f"./experiments/run{args.run}/results/llm_ic_pddl/{domain.name}"

    os.makedirs(problem_folder, exist_ok=True)
    os.makedirs(plan_folder, exist_ok=True)
    os.makedirs(result_folder, exist_ok=True)

    task = args.task

    start_time = time.time()

    # A. generate domain and problem pddl files
    task_suffix = domain.get_task_suffix(task)
    task_nl, _ = domain.get_task(task)
    prompt = planner.create_llm_ic_pddl_prompt(task_nl, domain_pddl, context)
    
    # Log the prompt
    logger.log_prompt(prompt)
    
    raw_result = planner.query(prompt)
    
    # Log the LLM response
    logger.log_llm_response(raw_result)
    
    domain_pddl_, task_pddl_ = planner.parse_domain_problem_result(raw_result)
    
    # Log the generated PDDL files
    logger.log_generated_pddl(domain_pddl_, task_pddl_)

    # B. write both domain and problem files
    task_domain_file_name = f"./experiments/run{args.run}/problems/llm_ic_pddl/{task_suffix.replace('.pddl', '_domain.pddl')}"
    task_pddl_file_name = f"./experiments/run{args.run}/problems/llm_ic_pddl/{task_suffix}"
    
    with open(task_domain_file_name, "w") as f:
        f.write(domain_pddl_)
    with open(task_pddl_file_name, "w") as f:
        f.write(task_pddl_)
    time.sleep(1)

    ## C. run fastforward to plan
    plan_file_name = f"./experiments/run{args.run}/plans/llm_ic_pddl/{task_suffix}"
    sas_file_name  = f"./experiments/run{args.run}/plans/llm_ic_pddl/{task_suffix}.sas"
    
    command = f"python ./downward-release-24.06.1/downward-release-24.06.1/fast-downward.py --alias {FAST_DOWNWARD_ALIAS} " + \
              f"--plan-file {plan_file_name} " + \
              f"--sas-file {sas_file_name} " + \
              f"{task_domain_file_name} {task_pddl_file_name}"
    
    # Capture planner output for logging
    exit_code, planner_output, planner_errors = run_command_with_timeout(command, timeout_seconds=args.time_limit, capture_output=True)
    
    # Log planner execution details
    logger.log_planner_execution(command, planner_output, planner_errors, exit_code)
    
    # Also print to console for immediate feedback
    if planner_output:
        print(planner_output)
    if planner_errors:
        print(planner_errors)
    
    if exit_code == -1:
        print(f"Planning timed out after {args.time_limit} seconds")
    elif exit_code != 0:
        print(f"Planning failed with exit code: {exit_code}")

    # D. collect the least cost plan
    best_cost = 1e10
    best_plan = None
    for fn in glob.glob(f"{plan_file_name}"):
        with open(fn, "r") as f:
            try:
                plans = f.readlines()
                cost = get_cost(plans[-1])
                if cost < best_cost:
                    best_cost = cost
                    best_plan = "\n".join([p.strip() for p in plans[:-1]])
            except:
                continue

    # E. Log results and save
    end_time = time.time()
    execution_time = end_time - start_time
    
    if best_plan:
        print(f"[info] task {task} takes {execution_time} sec, found a plan with cost {best_cost}")
        logger.log_plan_result(True, best_cost, best_plan)
    else:
        print(f"[info] task {task} takes {execution_time} sec, no solution found")
        logger.log_plan_result(False)
    
    logger.log_execution_time(execution_time)
    logger.save_logs()

def llm_pddl_planner(args, planner, domain):
    """
    Baseline method:
        Same as ours, except that no context is given. In other words, the LLM
        will be asked to directly generate both domain and problem PDDL files without any context.
    """
    domain_nl = domain.get_domain_nl()
    
    # Initialize logger
    log_dir = f"./logs/run{args.run}"
    logger = Logger(log_dir, args.task, "llm_pddl")
    
    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm_pddl/{domain.name}"
    plan_folder = f"./experiments/run{args.run}/plans/llm_pddl/{domain.name}"
    result_folder  = f"./experiments/run{args.run}/results/llm_pddl/{domain.name}"

    os.makedirs(problem_folder, exist_ok=True)
    os.makedirs(plan_folder, exist_ok=True)
    os.makedirs(result_folder, exist_ok=True)

    task = args.task

    start_time = time.time()

    # A. generate domain and problem pddl files
    task_suffix = domain.get_task_suffix(task)
    task_nl, _ = domain.get_task(task)
    prompt = planner.create_llm_pddl_prompt(task_nl, domain_nl)
    
    # Log the prompt
    logger.log_prompt(prompt)
    
    raw_result = planner.query(prompt)
    
    # Log the LLM response
    logger.log_llm_response(raw_result)
    
    domain_pddl_, task_pddl_ = planner.parse_domain_problem_result(raw_result)
    
    # Log the generated PDDL files
    logger.log_generated_pddl(domain_pddl_, task_pddl_)

    # B. write both domain and problem files
    task_domain_file_name = f"./experiments/run{args.run}/problems/llm_pddl/{task_suffix.replace('.pddl', '_domain.pddl')}"
    task_pddl_file_name = f"./experiments/run{args.run}/problems/llm_pddl/{task_suffix}"
    
    with open(task_domain_file_name, "w") as f:
        f.write(domain_pddl_)
    with open(task_pddl_file_name, "w") as f:
        f.write(task_pddl_)
    time.sleep(1)

    # C. run fastforward to plan
    plan_file_name = f"./experiments/run{args.run}/plans/llm_pddl/{task_suffix}"
    sas_file_name  = f"./experiments/run{args.run}/plans/llm_pddl/{task_suffix}.sas"
    
    command = f"python ./downward-release-24.06.1/downward-release-24.06.1/fast-downward.py --alias {FAST_DOWNWARD_ALIAS} " + \
              f"--plan-file {plan_file_name} " + \
              f"--sas-file {sas_file_name} " + \
              f"{task_domain_file_name} {task_pddl_file_name}"
    
    # Capture planner output for logging
    exit_code, planner_output, planner_errors = run_command_with_timeout(command, timeout_seconds=args.time_limit, capture_output=True)
    
    # Log planner execution details
    logger.log_planner_execution(command, planner_output, planner_errors, exit_code)
    
    # Also print to console for immediate feedback
    if planner_output:
        print(planner_output)
    if planner_errors:
        print(planner_errors)
    
    if exit_code == -1:
        print(f"Planning timed out after {args.time_limit} seconds")
    elif exit_code != 0:
        print(f"Planning failed with exit code: {exit_code}")

    # D. collect the least cost plan
    best_cost = 1e10
    best_plan = None
    for fn in glob.glob(f"{plan_file_name}"):
        with open(fn, "r") as f:
            try:
                plans = f.readlines()
                cost = get_cost(plans[-1])
                if cost < best_cost:
                    best_cost = cost
                    best_plan = "\n".join([p.strip() for p in plans[:-1]])
            except:
                continue

    # E. Log results and save
    end_time = time.time()
    execution_time = end_time - start_time
    
    if best_plan:
        print(f"[info] task {task} takes {execution_time} sec, found a plan with cost {best_cost}")
        logger.log_plan_result(True, best_cost, best_plan)
    else:
        print(f"[info] task {task} takes {execution_time} sec, no solution found")
        logger.log_plan_result(False)
    
    logger.log_execution_time(execution_time)
    logger.save_logs()

def llm_planner(args, planner, domain):
    """
    Baseline method:
        The LLM will be asked to directly give a plan based on the task description.
    """
    domain_nl = domain.get_domain_nl()
    
    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm/{domain.name}"
    plan_folder = f"./experiments/run{args.run}/plans/llm/{domain.name}"
    result_folder = f"./experiments/run{args.run}/results/llm/{domain.name}"

    os.makedirs(problem_folder, exist_ok=True)
    os.makedirs(plan_folder, exist_ok=True)
    os.makedirs(result_folder, exist_ok=True)

    task = args.task

    start_time = time.time()

    # A. generate problem pddl file
    task_suffix = domain.get_task_suffix(task)
    task_nl, _ = domain.get_task(task) 
    prompt = planner.create_llm_prompt(task_nl, domain_nl)
    text_plan = planner.query(prompt)

    # B. write the problem file into the problem folder
    text_plan_file_name = f"./experiments/run{args.run}/results/llm/{task_suffix}"
    with open(text_plan_file_name, "w") as f:
        f.write(text_plan)
    end_time = time.time()
    print(f"[info] task {task} takes {end_time - start_time} sec")

def llm_ic_planner(args, planner, domain):
    """
    Baseline method:
        The LLM will be asked to directly give a plan based on the task description.
    """
    context          = domain.get_context()
    domain_nl        = domain.get_domain_nl()

    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm_ic/{domain.name}"
    plan_folder    = f"./experiments/run{args.run}/plans/llm_ic/{domain.name}"
    result_folder  = f"./experiments/run{args.run}/results/llm_ic/{domain.name}"

    os.makedirs(problem_folder, exist_ok=True)
    os.makedirs(plan_folder, exist_ok=True)
    os.makedirs(result_folder, exist_ok=True)

    task = args.task

    start_time = time.time()

    # A. generate problem pddl file
    task_suffix        = domain.get_task_suffix(task)
    task_nl, _ = domain.get_task(task) 
    prompt             = planner.create_llm_ic_prompt(task_nl, domain_nl, context)
    text_plan          = planner.query(prompt)

    # B. write the problem file into the problem folder
    text_plan_file_name = f"./experiments/run{args.run}/results/llm_ic/{task_suffix}"
    with open(text_plan_file_name, "w") as f:
        f.write(text_plan)
    end_time = time.time()
    print(f"[info] task {task} takes {end_time - start_time} sec")

def print_all_prompts(planner):
    domain = Blocksworld()
    context = domain.get_context()
    domain_pddl = domain.get_domain_pddl()
    domain_nl = domain.get_domain_nl()
    
    for folder_name in [
        f"./prompts/llm/{domain.name}",
        f"./prompts/llm_ic/{domain.name}",
        f"./prompts/llm_pddl/{domain.name}",
        f"./prompts/llm_ic_pddl/{domain.name}"]:
        
        os.makedirs(folder_name, exist_ok=True)

    for task in range(len(domain)):
        task_nl, _ = domain.get_task(task) 
        task_suffix = domain.get_task_suffix(task)

        llm_prompt = planner.create_llm_prompt(task_nl, domain_nl)
        llm_ic_prompt = planner.create_llm_ic_prompt(task_nl, domain_nl, context)
        llm_pddl_prompt = planner.create_llm_pddl_prompt(task_nl, domain_nl)
        llm_ic_pddl_prompt = planner.create_llm_ic_pddl_prompt(task_nl, domain_pddl, context)
        
        with open(f"./prompts/llm/{task_suffix}.prompt", "w") as f:
            f.write(llm_prompt)
        with open(f"./prompts/llm_ic/{task_suffix}.prompt", "w") as f:
            f.write(llm_ic_prompt)
        with open(f"./prompts/llm_pddl/{task_suffix}.prompt", "w") as f:
            f.write(llm_pddl_prompt)
        with open(f"./prompts/llm_ic_pddl/{task_suffix}.prompt", "w") as f:
            f.write(llm_ic_pddl_prompt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM-Planner")
    parser.add_argument('--domain', type=str, choices=["blocksworld"], default="blocksworld")
    parser.add_argument('--method', type=str, choices=["llm_ic_pddl_planner",
                                                       "llm_pddl_planner",
                                                       "llm_planner",
                                                       "llm_ic_planner"],
                                              default="llm_planner")
    parser.add_argument('--time-limit', type=int, default=200)
    parser.add_argument('--task', type=int, default=0)
    parser.add_argument('--run', type=int, default=2)
    parser.add_argument('--print-prompts', action='store_true')
    args = parser.parse_args()

    # 1. initialize problem domain
    domain = Blocksworld()

    # 2. initialize the planner
    planner = Planner()

    # 3. execute the llm planner
    method = {
        "llm_ic_pddl_planner" : llm_ic_pddl_planner,
        "llm_pddl_planner" : llm_pddl_planner,
        "llm_planner" : llm_planner,
        "llm_ic_planner" : llm_ic_planner
    }[args.method]

    if args.print_prompts:
        print_all_prompts(planner)
    else:
        method(args, planner, domain)
