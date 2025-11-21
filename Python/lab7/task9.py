import math

def solve_quadratic(a, b, c):
    if a == 0:
        return "Not a quadratic equation because a = 0"

    D = b**2 - 4 * a * c

    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)
        return f"Two solutions: x1 = {x1}, x2 = {x2}"
    elif D == 0:
        x = -b / (2 * a)
        return f"One solution: x = {x}"
    else:
        return "No real roots"

a = 1
b = -3
c = 2
solution = solve_quadratic(a, b, c)
print(solution)