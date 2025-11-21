import matplotlib.pyplot as plt

def generate_fibonacci(n):
    fibonacci_sequence = []
    a, b = 0, 1
    for _ in range(n):
        fibonacci_sequence.append(a)
        a, b = b, a + b
    return fibonacci_sequence

n = int(input("Enter the number of Fibonacci sequence terms: "))
fibonacci_numbers = generate_fibonacci(n)
print("First", n, "terms of the Fibonacci sequence: ", fibonacci_numbers)

plt.figure(figsize=(10, 6))
plt.plot(range(n), fibonacci_numbers, marker='o', color='b', linestyle='-')
plt.title("Dependence of the Fibonacci sequence term position on its value")
plt.xlabel("Position of the sequence term")
plt.ylabel("Value of the Fibonacci sequence term")
plt.grid()
plt.show()