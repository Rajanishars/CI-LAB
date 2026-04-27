import random

def coin_toss_probability():
    n = int(input("Enter the number of coin tosses: "))

    heads = 0
    tails = 0

    for i in range(n):
        toss = random.choice(['H', 'T'])
        print(f"Toss {i+1}: {toss}")

        if toss == 'H':
            heads += 1
        else:
            tails += 1

    print("\nResults:")
    print("Number of Heads:", heads)
    print("Number of Tails:", tails)

    print("\nProbabilities:")
    print("P(Heads) =", heads / n)
    print("P(Tails) =", tails / n)

coin_toss_probability()
