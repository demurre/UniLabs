a, b = 2.58, 12.4

x = float(input("x: "))
y = float(input("y: "))

if x < y:
    t = (a + b) / 2 - a**2 + b**3
    print(f"x < y, so t = (a + b)/2 - a^2 + b^3 = {t}")
elif x > y:
    t = (a + b / 2) / 2
    print(f"x > y, so t = (a + b/2)/2 = {t}")
else:
    t = 3.2
    print(f"x = y, so t = 3.2")
