import math

a = float(input("a: "))
b = float(input("b: "))
c = float(input("c: "))

D = b**2 - 4 * a * c
if D > 0:
    x1 = (-b + math.sqrt(D)) / (2 * a)
    x2 = (-b - math.sqrt(D)) / (2 * a)
    print(f"x1 = {x1:.2f}, x2 = {x2:.2f}")
elif D == 0:
    x = -b / (2 * a)
    print(f"x = {x:.2f}")
else:
    print("The equation has no real roots")
