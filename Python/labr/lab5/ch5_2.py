import math


def main():
    try:
        calculate_sphere_volume = lambda r: (4 / 3) * math.pi * r**3

        print_header = lambda: print(
            "=" * 40 + "\nCALCULATING THE VOLUME OF A SPHERE\n" + "=" * 40
        )

        format_result = lambda volume: f"Sphere volume: {volume:.4f} cubic units"
        format_formula = lambda: "Calculation formula: V = (4/3) * π * r^3"

        print_header()

        r = float(input("\nEnter the radius of the sphere (r): "))

        if r <= 0:
            print("Error: radius must be a positive number.")
            return

        volume = calculate_sphere_volume(r)

        print("\n" + format_formula())
        print(f"For radius r = {r}")
        print(format_result(volume))

    except ValueError:
        print("Error: enter a valid numeric value for the radius.")


if __name__ == "__main__":
    main()
