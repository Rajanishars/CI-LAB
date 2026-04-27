from itertools import product

def parse_condition(cond):
    cond = cond.strip().lower()
    if cond.startswith('~'):
        return cond[1:], False
    return cond, True

def check_conditions(row, conditions):
    for var, val in conditions:
        if var not in row:
            continue
        if row[var] != val:
            return False
    return True

def normalize_kb(kb):
    """Convert counts → probabilities if needed"""
    total = sum(row['prob'] for row in kb)

    if total == 0:
        raise ValueError("Total probability/count cannot be zero.")

    for row in kb:
        row['prob'] /= total

def compute_probability(kb, query_conditions, given_conditions=None):
    numerator = 0
    denominator = 0

    if given_conditions is None:
        # P(A)
        for row in kb:
            if check_conditions(row, query_conditions):
                numerator += row['prob']
        return round(numerator, 4)

    else:
        # P(A | B) = P(A ∧ B) / P(B)
        for row in kb:
            if check_conditions(row, given_conditions):
                denominator += row['prob']
                if check_conditions(row, query_conditions):
                    numerator += row['prob']

        return round(numerator / denominator, 4) if denominator != 0 else 0

def main():
    num_vars = int(input("Enter number of variables: ").strip())

    variables = []
    print("Enter variable names:")
    for _ in range(num_vars):
        variables.append(input().strip().lower())

    combinations = list(product([True, False], repeat=num_vars))
    kb = []

    print("\nEnter probabilities OR counts for each combination:")
    for comb in combinations:
        row = {}
        display_parts = []

        for i, val in enumerate(comb):
            row[variables[i]] = val
            display_parts.append(f"{variables[i]}={'T' if val else 'F'}")

        print(", ".join(display_parts))
        row['prob'] = float(input("Value: "))
        kb.append(row)


    normalize_kb(kb)

    print("\n--- Query Section ---")
    print("Examples: P(a), P(a|b), P(a,~b|c)")

    while True:
        raw_query = input("\nEnter query (or 'exit'): ").strip().lower()
        if raw_query == 'exit':
            break

        clean_query = raw_query.replace("p(", "").replace(")", "")

        if '|' in clean_query:
            left, right = clean_query.split('|')
            query_vars = [parse_condition(c) for c in left.split(',')]
            given_vars = [parse_condition(c) for c in right.split(',')]
            result = compute_probability(kb, query_vars, given_vars)
        else:
            query_vars = [parse_condition(c) for c in clean_query.split(',')]
            result = compute_probability(kb, query_vars)

        print(f"Result = {result}")

if __name__ == "__main__":
    main()
