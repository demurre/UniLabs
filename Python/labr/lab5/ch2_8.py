import math


def calculate_circle_area(radius):
    if radius <= 0:
        raise ValueError("The radius must be a positive number")

    area = math.pi * radius**2
    return area


def main():
    try:
        radius = float(input("Enter the radius of the circle: "))

        circle_area = calculate_circle_area(radius)

        print(f"Area of a circle with radius {radius} equals {circle_area:.4f} sq. m.")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
