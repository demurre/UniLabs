import math

x = float(input("x: "))
y = float(input("y: "))

if x < 1.5:
    z = (x**2 + y**2) / (x * y)
    print("x<1.5, z({}, {}) = {:.4f}".format(x, y, z))
elif x >= 1.5:
    z = (x**2 + y**2) * math.exp(x * y)
    print("x>=1.5, z({}, {}) = {:.4f}".format(x, y, z))
else:
    print("Incorrect values")
