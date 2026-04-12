import math

def read_data(filename):
    with open(filename, "r") as file:
        lines = file.read().strip().split("\n")
    headers = lines[0].split(",")
    data = [line.split(",") for line in lines[1:]]
    return headers, data

def entropy(values):
    total = len(values)
    if total == 0: return 0
    ent = 0
    unique = list(set(values))
    for u in unique:
        p = values.count(u) / total
        ent -= p * math.log2(p)
    return ent

def get_gain_and_print(data, attr_index, target_index, total_entropy, attr_name, verbose=False):
    values = sorted(list(set(row[attr_index] for row in data)))
    total_records = len(data)
    weighted_entropy = 0

    if verbose:
        print(f"\nAttribute: {attr_name}")
        print("Value\tYes\tNo\tEntropy Formula")

    for val in values:
        subset = [row[target_index] for row in data if row[attr_index] == val]
        y = subset.count("yes")
        n = subset.count("no")
        t = len(subset)
        ent = entropy(subset)
        weighted_entropy += (t / total_records) * ent

        if verbose:
            if y == 0 or n == 0:
                formula = "0.0"
            else:
                formula = f"-({y}/{t}log2({y}/{t})) - ({n}/{t}log2({n}/{t})) = {round(ent, 4)}"
            print(f"{val}\t{y}\t{n}\t{formula}")

    gain = total_entropy - weighted_entropy
    if verbose:
        print(f"\nWeighted Entropy = {round(weighted_entropy, 4)}")
        print(f"Information Gain = {round(gain, 4)}")

    return gain

def build_tree(data, headers, is_root=False):
    target_values = [row[-1] for row in data]

    if len(set(target_values)) == 1:
        return target_values[0]

    if len(headers) == 1:
        return max(set(target_values), key=target_values.count)

    target_idx = len(headers) - 1
    total_ent = entropy(target_values)

    if is_root:
        print(f"Target Attribute: {headers[target_idx]}")
        print(f"Total Entropy = {round(total_ent, 4)}")

    gains = {}
    for i in range(target_idx):
        gain = get_gain_and_print(data, i, target_idx, total_ent, headers[i], verbose=is_root)
        gains[headers[i]] = gain

    if is_root:
        print("\nSummary of Information Gain")
        for attr, g in gains.items():
            print(f"{attr} : {round(g, 4)}")

    best_attr_name = max(gains, key=gains.get)
    best_attr_idx = headers.index(best_attr_name)

    if is_root:
        print(f"\nRoot Node: {best_attr_name}")

    tree = {best_attr_name: {}}
    attr_values = sorted(list(set(row[best_attr_idx] for row in data)))

    for val in attr_values:
        subset = [row[:best_attr_idx] + row[best_attr_idx+1:] for row in data if row[best_attr_idx] == val]
        new_headers = headers[:best_attr_idx] + headers[best_attr_idx+1:]
        tree[best_attr_name][val] = build_tree(subset, new_headers, is_root=False)

    return tree

def print_formatted_tree(tree, indent=""):
    if not isinstance(tree, dict):
        print(f" -> Result: {tree}")
        return

    for node, branches in tree.items():
        if indent == "":
            print(f"[{node}]")

        for value, subtree in branches.items():
            print(f"{indent}  |-- {value}", end="")
            if isinstance(subtree, dict):
                next_node = list(subtree.keys())[0]
                print(f"  |   [{next_node}]")
                print_formatted_tree(subtree, indent + "  |     ")
            else:
                print_formatted_tree(subtree, indent + "  |     ")

# --- Execution ---
headers, data = read_data("data.txt")
full_tree = build_tree(data, headers, is_root=True)

print("\n--- Generated Decision Tree ---")
print_formatted_tree(full_tree)
