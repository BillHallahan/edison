import re
import os

def process_co_ordinates(pairs):
    res = ""
    for (time, height) in pairs:
        res += "(" + str(time) + ", " + str(height) + ")"
    return res


def read_output(setname):
    symbolic = ""
    cons = ""

    dict = {}
    dict_constraints = {}
    dict_unrolling = {}

    current_dir = os.getcwd()

    file_path = os.path.join(current_dir, setname)
    print(file_path)

    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if ":" in line:
                    prop, value = line.split(":", 1)
                    time_str = value.strip().strip(",")
                    time = float(time_str.strip()) if time_str else -0.0
                    prop_n = prop.strip()
                    dict[prop_n] = time

    for key, value in dict.items():
        prop = key.replace("_symbolic", "").replace("_sym_constraints", "").replace("_", "\_")
        if "_symbolic" in key:
            print(prop + ",")
            dict_unrolling[prop] = value
            symbolic += "(" + prop + ", " + str(value) + ")"
        else:
            dict_constraints[prop] = value
            cons += "(" + prop + ", " + str(value) + ")"

    return (symbolic, cons, dict_constraints, dict_unrolling)

def largestUnrollingBetter(dict_constraints, dict_unrolling):
    best_prop = ""
    best_score = 0
    for prop in dict_unrolling:
        score = dict_constraints[prop] - dict_unrolling[prop]
        if score > best_score:
            best_score = score
            best_prop = prop
    
    print("" \
    "Largest better performance unrolling:" + str(best_prop) + " by " + str(best_score))

def compareResults(dict_constraints, dict_unrolling, tolerance):
    constraints_beats_unrolling = 0
    unrolling_beats_constraints = 0
    for prop in dict_unrolling:
        if (dict_constraints[prop] + tolerance < dict_unrolling[prop] and dict_constraints[prop] != 0) or dict_unrolling[prop] == 0:
            constraints_beats_unrolling += 1
        elif (dict_unrolling[prop] + tolerance < dict_constraints[prop] and dict_unrolling[prop] != 0) or dict_constraints[prop] == 0:
            unrolling_beats_constraints += 1
    print("\nTolerance:" + str(tolerance))
    print ("Constraints faster: " + str(constraints_beats_unrolling))
    print ("Unrolling faster: " + str(unrolling_beats_constraints))

(symbolic_data, func_cons_data, dict_constraints, dict_unrolling) = read_output("test/logs/state_accept_log.txt")

compareResults(dict_constraints, dict_unrolling, 0)
compareResults(dict_constraints, dict_unrolling, 0.1)
compareResults(dict_constraints, dict_unrolling, 1)
compareResults(dict_constraints, dict_unrolling, 10)
largestUnrollingBetter(dict_constraints, dict_unrolling)

print("\nFunc Constraints co-ordinates for counter-example")
print(func_cons_data)

print("\nSymbolic co-ordinates for counter-example")
print(symbolic_data)