import math

a, b, c = 7.84, 6.93, 8.07
p = (a + b + c) / 2
s = math.sqrt(p * (p - a) * (p - b) * (p - c))

print("The sides of the triangle: a = {}, b = {}, c = {}".format(a, b, c))
print("Area of a triangle: {:.4f}".format(s))
