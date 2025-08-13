import glob
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


print("FUCK YOU\n")

plan_file_name = f'E:\projects\MSc_project\Blockworld_task\llm_pddl_framework\experiments\run2\plans\llm_ic_pddl\blocksworld\p03.pddl'
# print(f"Reading plans from {plan_file_name}")

best_cost = 1e10

for fn in glob.glob(f"{plan_file_name}"):
    with open(fn, "r") as f:
        try:
            plans = f.readlines()
            print(plans[-1])
            cost = get_cost(plans[-1])
            # print(plans[-1].strip())
            if cost < best_cost:
                best_cost = cost
                # best_plan = "\n".join([p.strip() for p in plans[:-1]])
        except:
            continue

print(best_cost)