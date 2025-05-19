import math


def calculate_cone_surface_area():
    try:
        r = float(input("Enter the radius of the base of the cone (r): "))
        l = float(input("Enter the length of the cone shape (l): "))

        if r <= 0 or l <= 0:
            return "Error: radius and product must be positive numbers."

        base_area = math.pi * r**2

        lateral_area = math.pi * r * l

        total_surface_area = base_area + lateral_area

        return f"Surface area of the cone: {total_surface_area:.4f} sq. m."

    except ValueError:
        return "Error: Enter numeric values for the radius and the product."


if __name__ == "__main__":
    result = calculate_cone_surface_area()
    print(result)
