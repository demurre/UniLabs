import math

class Rhombus:
    def __init__(self):
        pass

    def menu(self):
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
                result = self.calculate_cube_surface_area()
                print(f"Cube surface area: {result}")
            elif choice == 2:
                result = self.calculate_rhombus_area()
                print(f"Rhombus area: {result}")
            elif choice == 3:
                result = self.volume_cone()
                print(f"Cone volume: {round(result, 3)}")
            elif choice == 4:
                result = self.fibonacci_number()
                print(f"Fibonacci number: {result}")
            elif choice == 5:
                result = self.solve_equation()
                print(result)
            elif choice == 6:
                print("Exiting program.")
                break
            else:
                print("Invalid mode number. Enter a number from 1 to 6.")

    # #1: Cube surface area
    def calculate_cube_surface_area(self):
        try:
            a = float(input("Enter the length of the cube edge (a): "))
            S = 6 * (a ** 2)
            return S
        except ValueError:
            print("Invalid input. Enter a numeric value.")

    # #7: Rhombus area using diagonals
    def get_initial_conditions(self):
        try:
            d1 = float(input("Enter the length of the first diagonal of the rhombus (d1): "))
            d2 = float(input("Enter the length of the second diagonal of the rhombus (d2): "))
            return d1, d2
        except ValueError:
            print("Invalid input. Enter numeric values.")
            return None, None

    def calculate_rhombus_area(self):
        d1, d2 = self.get_initial_conditions()
        if d1 is not None and d2 is not None:
            area = 0.5 * d1 * d2
            return area

    # #12: Cone volume
    def volume_cone(self):
        print_title = lambda: print("Calculating cone volume")
        volume_cone = lambda r, l: (1/3) * math.pi * (r**2) * l
        try:
            print_title()
            r = float(input("Enter the radius of the cone base (r): "))
            l = float(input("Enter the height of the cone (l): "))
            volume = volume_cone(r, l)
            return volume
        except ValueError:
            print("Invalid input. Enter numeric values.")

    # #4: Fibonacci number
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
            return result
        except ValueError:
            print("Invalid input. Enter an integer.")

    # #8: Solving the equation ax + b = 0
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
                return x
        except ValueError:
            print("Invalid input. Enter numeric values.")


rhombus = Rhombus()
rhombus.menu()
