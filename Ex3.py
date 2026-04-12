import csv
import math

def distance_metric(p1, p2, r):
    total = 0
    if r == 1:   # Euclidean
        for i in range(len(p1)):
            diff = p1[i] - p2[i]
            total += diff * diff
        return math.sqrt(total)
    else:        # Manhattan
        for i in range(len(p1)):
            total += abs(p1[i] - p2[i])
        return total


def load_iris(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                features = list(map(float, row[:-1]))
                data.append(features + [row[-1]])
    return data



def normalize(data):
    mins, maxs = [], []

    for i in range(len(data[0]) - 1):
        col = [row[i] for row in data]
        mins.append(min(col))
        maxs.append(max(col))

    norm = []
    for row in data:
        new_row = []
        for i in range(len(row) - 1):
            val = (row[i] - mins[i]) / (maxs[i] - mins[i])
            new_row.append(val)
        new_row.append(row[-1])
        norm.append(new_row)

    return norm, mins, maxs

def knn_weighted(train, query, k, r):
    distances = []

    for row in train:
        d = distance_metric(row[:-1], query, r)
        distances.append([d, row[-1]])

    distances.sort(key=lambda x: x[0])
    neighbors = distances[:k]

    weights = {}
    for item in neighbors:
        d = item[0]
        label = item[1]
        weight = 1 / (d + 0.00001)

        if label in weights:
            weights[label] += weight
        else:
            weights[label] = weight

    return max(weights, key=weights.get)


def knn_unweighted(train, query, k, r):
    distances = []

    for row in train:
        d = distance_metric(row[:-1], query, r)
        distances.append([d, row[-1]])

    distances.sort(key=lambda x: x[0])
    neighbors = distances[:k]

    votes = {}
    for item in neighbors:
        label = item[1]
        if label in votes:
            votes[label] += 1
        else:
            votes[label] = 1

    return max(votes, key=votes.get)


def print_full_table(results, weighted):
    print("\n--- FULL DATASET (150 POINTS) ---\n")

    if weighted:
        header = (
            f"{'P#':<7}{'F1':<6}{'F2':<6}{'F3':<6}{'F4':<6}"
            f"{'Dist':<8}{'Weight':<9}"
            f"{'NF1':<7}{'NF2':<7}{'NF3':<7}{'NF4':<7}"
            f"{'Class':<18}{'Rank'}"
        )
    else:
        header = (
            f"{'P#':<7}{'F1':<6}{'F2':<6}{'F3':<6}{'F4':<6}"
            f"{'Dist':<8}"
            f"{'NF1':<7}{'NF2':<7}{'NF3':<7}{'NF4':<7}"
            f"{'Class':<18}{'Rank'}"
        )

    print(header)
    print("-" * len(header))

    for i, r in enumerate(results, start=1):
        if weighted:
            print(
                f"{'P'+str(i):<6}"
                f"{r['f1']:<6.1f}{r['f2']:<6.1f}{r['f3']:<6.1f}{r['f4']:<6.1f}"
                f"{r['dist']:<8.4f}{r['weight']:<9.4f}"
                f"{r['nf1']:<7.3f}{r['nf2']:<7.3f}{r['nf3']:<7.3f}{r['nf4']:<7.3f}"
                f"{r['class']:<18}{i}"
            )
        else:
            print(
                f"{'P'+str(i):<6}"
                f"{r['f1']:<6.1f}{r['f2']:<6.1f}{r['f3']:<6.1f}{r['f4']:<6.1f}"
                f"{r['dist']:<8.4f}"
                f"{r['nf1']:<7.3f}{r['nf2']:<7.3f}{r['nf3']:<7.3f}{r['nf4']:<7.3f}"
                f"{r['class']:<18}{i}"
            )



def print_k_neighbors(results, k, weighted):
    print(f"\n--- K = {k} NEAREST NEIGHBORS ---\n")

    if weighted:
        header = (
            f"{'P#':<4}{'F1':<6}{'F2':<6}{'F3':<6}{'F4':<6}"
            f"{'Dist':<8}{'Weight':<9}"
            f"{'Class':<18}{'Rank'}"
        )
    else:
        header = (
            f"{'P#':<4}{'F1':<6}{'F2':<6}{'F3':<6}{'F4':<6}"
            f"{'Dist':<8}"
            f"{'Class':<18}{'Rank'}"
        )

    print(header)
    print("-" * len(header))

    for i in range(k):
        r = results[i]
        if weighted:
            print(
                f"P{i+1:<3}"
                f"{r['f1']:<6.1f}{r['f2']:<6.1f}{r['f3']:<6.1f}{r['f4']:<6.1f}"
                f"{r['dist']:<8.4f}{r['weight']:<9.4f}"
                f"{r['class']:<18}{i+1}"
            )
        else:
            print(
                f"P{i+1:<3}"
                f"{r['f1']:<6.1f}{r['f2']:<6.1f}{r['f3']:<6.1f}{r['f4']:<6.1f}"
                f"{r['dist']:<8.4f}"
                f"{r['class']:<18}{i+1}"
            )

def main():
    data = load_iris("iris.csv")
    norm_data, mins, maxs = normalize(data)
    print("\n---Feautures Classification ---")
    print(f"Feature Ranges: F1({mins[0]}-{maxs[0]}), F2({mins[1]}-{maxs[1]}), F3({mins[2]}-{maxs[2]}), F4({mins[3]}-{maxs[3]})")
    print("\nF1=Body_Adiposity_Index, F2=Creatinine_Level, F3=HbA1c_Pct, F4=Albumin_Ratio, Target:Diagnosis(A:Healthy/B:Risk)")

    print("\nEnter Query Features:")
    query = [float(input(f"Feature {i+1}: ")) for i in range(4)]

    query_norm = [(query[i] - mins[i]) / (maxs[i] - mins[i]) for i in range(4)]

    r = int(input("Distance (1-Euclidean, 2-Manhattan): "))
    vote_type = int(input("Voting (1-Unweighted, 2-Weighted): "))

    weighted = (vote_type == 2)
    results = []

    for i in range(len(data)):
        dist = distance_metric(norm_data[i][:-1], query_norm, r)

        if weighted:
            weight = 1 / (dist + 0.00001)
        else:
            weight = None

        results.append({
            'f1': data[i][0], 'f2': data[i][1],
            'f3': data[i][2], 'f4': data[i][3],
            'nf1': norm_data[i][0], 'nf2': norm_data[i][1],
            'nf3': norm_data[i][2], 'nf4': norm_data[i][3],
            'dist': dist,
            'weight': weight,
            'class': data[i][4]
        })

    results.sort(key=lambda x: x['dist'])

    print_full_table(results, weighted)
    print()
    k = int(input("Enter K value: "))
    print_k_neighbors(results, k, weighted)

    print("\nClass-wise Count (among K neighbors):")
    class_count = {}

    for i in range(k):
        cls = results[i]['class']
        class_count[cls] = class_count.get(cls, 0) + 1

    for cls in class_count:
        print(f"{cls:<18} ->{class_count[cls]}")

    if weighted:
        class_weights = {}
        for i in range(k):
            cls = results[i]['class']
            class_weights[cls] = class_weights.get(cls, 0) + results[i]['weight']

        print("\nClass-wise Weights:")
        for cls in class_weights:
            print(f"{cls:<18}: {class_weights[cls]:.4f}")

        predicted = max(class_weights, key=class_weights.get)
    else:
        votes = {}
        for i in range(k):
            cls = results[i]['class']
            votes[cls] = votes.get(cls, 0) + 1

        predicted = max(votes, key=votes.get)

    print("\nPredicted Class:", predicted)

if __name__ == "__main__":
    main()
