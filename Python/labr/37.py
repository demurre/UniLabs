def factorial(k):
    if k > 12:
        return "Error: k must be no more than 12."

    result = 1
    i = 1

    while True:
        result *= i
        i += 1
        if i > k:
            break

    return result


k = int(input("Enter the value of k (no more than 12): "))

factorial_result = factorial(k)

print(f"{k}! = {factorial_result}")
