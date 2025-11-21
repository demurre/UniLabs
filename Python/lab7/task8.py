def solve_equation(a, b):
    if a == 0:
        if b == 0:
            return "Many solutions (equation has infinitely many solutions)"
        else:
            return "No solutions"

    x = -b / a
    return f"Solution: x = {x}"

a = 2
b = -4
solution = solve_equation(a, b)
print(solution)