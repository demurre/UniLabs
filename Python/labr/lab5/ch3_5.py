import math


def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


def term_sinh_taylor(x, n):
    power = 2 * n + 1
    term = (x**power) / factorial(power)
    return term


def sinh_taylor_3_terms(x):
    result = 0
    for n in range(3):
        result += term_sinh_taylor(x, n)
    return result


def sinh_taylor_4_terms(x):
    result = 0
    for n in range(4):
        result += term_sinh_taylor(x, n)
    return result


def sinh_taylor_5_terms(x):
    result = 0
    for n in range(5):
        result += term_sinh_taylor(x, n)
    return result


def print_formulas():
    print("\nTaylor series expansion formulas for hyperbolic sine:")
    print("3 terms: sinh(x) ≈ x + x^3/3! + x^5/5!")
    print("4 terms: sinh(x) ≈ x + x^3/3! + x^5/5! + x^7/7!")
    print("5 terms: sinh(x) ≈ x + x^3/3! + x^5/5! + x^7/7! + x^9/9!")


def calculate_sinh():
    try:
        x = float(input("Enter the value of x to calculate sinh(x): "))

        sinh_3 = sinh_taylor_3_terms(x)
        sinh_4 = sinh_taylor_4_terms(x)
        sinh_5 = sinh_taylor_5_terms(x)

        exact_sinh = math.sinh(x)

        print(f"\nResults of calculating sinh({x}):")
        print(f"According to the Taylor formula (3 terms): {sinh_3}")
        print(f"According to the Taylor formula (4 terms): {sinh_4}")
        print(f"According to the Taylor formula (5 terms): {sinh_5}")
        print(f"Exact value (math.sinh): {exact_sinh}")

        print("\nAbsolute errors:")
        print(f"For 3 terms: {abs(exact_sinh - sinh_3)}")
        print(f"For 4 terms: {abs(exact_sinh - sinh_4)}")
        print(f"For 5 terms: {abs(exact_sinh - sinh_5)}")

        print_formulas()

    except ValueError:
        print("Error: enter a valid numeric value.")


if __name__ == "__main__":
    calculate_sinh()
