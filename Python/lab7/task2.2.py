def factorial(x):
    result = 1
    for i in range(2, x + 1):
        result *= i
    return result

def calculate_combinations(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

n= int(input("Enter value n: "))
k = int(input("Enter value k: "))
print("Number of combinations: ", calculate_combinations(n, k))