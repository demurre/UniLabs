import math

class Rhombus:
    def __init__(self):
        pass

    def calculate_cube_surface_area(self):
        try:
            a = float(input("Enter the length of the cube edge (a): "))
            S = 6 * (a ** 2)
            print(f"Cube surface area: {S}")
        except ValueError:
            print("Invalid input. Enter a numeric value.")

    def calculate_rhombus_area(self):
        try:
            d1 = float(input("Enter the length of the first diagonal of the rhombus (d1): "))
            d2 = float(input("Enter the length of the second diagonal of the rhombus (d2): "))
            area = 0.5 * d1 * d2
            print(f"Rhombus area: {area}")
        except ValueError:
            print("Invalid input. Enter numeric values.")

    def volume_cone(self):
        print_title = lambda: print("Calculating cone volume")
        volume_cone = lambda r, l: (1/3) * math.pi * (r**2) * l
        try:
            print_title()
            r = float(input("Enter the radius of the cone base (r): "))
            l = float(input("Enter the height of the cone (l): "))
            volume = volume_cone(r, l)
            print(f"Cone volume: {round(volume, 3)}")
        except ValueError:
            print("Invalid input. Enter numeric values.")

    def fibonacci(self, n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def fibonacci_number(self):
        try:
            n = int(input("Enter the position of the Fibonacci number (n): "))
            result = self.fibonacci(n)
            print(f"Fibonacci number at position {n}: {result}")
        except ValueError:
            print("Invalid input. Enter an integer.")

    def solve_equation(self):
        try:
            a = float(input("Enter coefficient a: "))
            b = float(input("Enter coefficient b: "))
            if a == 0:
                if b == 0:
                    print("Infinitely many solutions (0 = 0).")
                else:
                    print("No solutions (a = 0, b ≠ 0).")
            else:
                x = -b / a
                print(f"Solution of the equation: x = {x}")
        except ValueError:
            print("Invalid input. Enter numeric values.")

rhombus = Rhombus()

def main():
    while True:
        print("\nSelect a task to calculate:")
        print("1. Calculate the surface area of a cube")
        print("2. Calculate the area of a rhombus using diagonals")
        print("3. Calculate the volume of a cone")
        print("4. Find the Fibonacci number at position n")
        print("5. Solve the equation ax + b = 0")
        print("6. Exit")

        try:
            choice = int(input("Enter mode number: "))
        except ValueError:
            print("Invalid input. Enter a number from 1 to 6.")
            continue

        if choice == 1:
            rhombus.calculate_cube_surface_area()
        elif choice == 2:
            rhombus.calculate_rhombus_area()
        elif choice == 3:
            rhombus.volume_cone()
        elif choice == 4:
            rhombus.fibonacci_number()
        elif choice == 5:
            rhombus.solve_equation()
        elif choice == 6:
            print("Exiting program.")
            break
        else:
            print("Invalid mode number. Enter a number from 1 to 6.")


if __name__ == '__main__':
    main()
