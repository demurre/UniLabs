import math

def calculate_combinations(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

n= int(input("Enter value n: "))
k = int(input("Enter value k: "))
print("Number of combinations: ", calculate_combinations(n, k))