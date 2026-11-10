import re
import os

def process_co_ordinates(pairs):
    res = ""
    for (time, height) in pairs:
        res += "(" + str(time) + ", " + str(height) + ")"
    return res


def read_output(setname, timeout):
    symbolic = ""
    cons = ""
    coOrd_symbolic_bc = []
    coOrd_cons_bc = []

    dict = {}
    res_sym_constraints = {}
    res_symbolic = {}

    current_dir = os.getcwd()

    setpath = os.path.join(current_dir, setname)
    print(setpath)
    all_files = os.listdir(setpath);

    for filename in all_files:
        # print(filename)
        prop_name = filename.replace(".txt", "")
        # print(prop_name)
        file_path = os.path.join(setpath, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    sym = False
                    coOrds = re.findall(r"\(([^)]+)\)", line)
                    result = [tuple(map(float, pair.split(','))) for pair in coOrds]
                    filtered_list = [(float(x), int(y)) for x, y in result if float(x) <= timeout]
                    (time, height) = filtered_list[-1]
                    
                    property = prop_name.replace("_symbolic", "").replace("_sym_constraints", "")

                    if "_sym_constraints" in prop_name:
                        coOrd_cons_bc.append(((prop_name.replace("_sym_constraints", "").replace("_", "\_")), height))
                        res_sym_constraints[property] = (time, height)
                    else:
                        coOrd_symbolic_bc.append(((prop_name.replace("_symbolic", "").replace("_", "\_")), height))
                        sym = True
                        res_symbolic[property] = (time, height)
                        
                    # dict[prop_name] = "\\addplot[color=blue,mark=square,] coordinates { " + process_co_ordinates(filtered_list) + " };"

                    if property in dict:
                        (temp, isSym) = dict[property]
                        if isSym:
                            dict[property] = (("\\addplot[color=blue,mark=square,] coordinates { " + process_co_ordinates(filtered_list) + " }; " + temp), isSym)
                        else:
                            dict[property] = ((temp + " \\addplot[color=red,mark=circle,] coordinates { " + process_co_ordinates(filtered_list) + " }; "), isSym)

                    else:
                        if sym:
                            dict[property] = ("\\addplot[color=red,mark=circle,] coordinates { " + process_co_ordinates(filtered_list) + " };", sym)
                        else:
                            dict[property] = ("\\addplot[color=blue,mark=square,] coordinates { " + process_co_ordinates(filtered_list) + " };", sym)


    for (prop, height) in coOrd_symbolic_bc:
        print(prop + ",")
        symbolic += "(" + prop + ", " + str(height) + ")"
    for (prop, height) in coOrd_cons_bc:
        cons += "(" + prop + ", " + str(height) + ")"

    return (symbolic, cons, dict, res_sym_constraints, res_symbolic)


(symbolic_data, func_cons_data, line_graph_data, res_sym_constraints, res_symbolic) = read_output("test/logs/time_logs/", 300)

print("\nLine graph co-ordinates")
for key, value in line_graph_data.items():
    (plot, flag) = value
    print(key + ":")
    print(plot + "\n")

# output number at least doubled
at_least_doubled = 0
for prop in res_sym_constraints:
    (_, h_sc) = res_sym_constraints[prop]
    (_, h_unroll) = res_symbolic[prop]
    if h_sc >= h_unroll * 2:
        at_least_doubled += 1

print("Number of times height at least doubled: " + str(at_least_doubled))    

# output coordinates for bar charts
print("\n Func Constraints co-ordinates")
print(func_cons_data)

print("\nSymbolic co-ordinates")
print(symbolic_data)

