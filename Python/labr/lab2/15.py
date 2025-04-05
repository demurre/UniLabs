import math

x_values = [1, 2, 3]

for x in x_values:
    y = math.exp(1 / math.tan(x)) * (2 * x**2 + 9 * x + 4) ** 3
    print(f"At x = {x}, y = {y:.6f}")
