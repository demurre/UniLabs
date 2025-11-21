import math

print_title = lambda: print("Calculating cone volume")

volume_cone = lambda r, l: (1/3) * math.pi * (r**2) * l

print_title()

r = float(input("Enter the radius of the cone base (r): "))
l = float(input("Enter the height of the cone (l): "))

volume = volume_cone(r, l)
print(f"Cone volume: {volume}")
