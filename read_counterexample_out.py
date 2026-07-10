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
            symbolic += "(" + prop + ", " + str(value) + ")"
        else:
            cons += "(" + prop + ", " + str(value) + ")"

    return (symbolic, cons)


(symbolic_data, func_cons_data) = read_output("test/time_logs/state_accept_log.txt")

print("\nFunc Constraints co-ordinates for counter-example")
print(func_cons_data)

print("\nSymbolic co-ordinates for counter-example")
print(symbolic_data)