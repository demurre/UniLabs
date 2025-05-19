import math


def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)


def calculate_term(x, k):
    return ((-1) ** (k + 1)) * (x**k) / k


def ln_taylor(x, terms):
    if not (0 < x <= 2):
        raise ValueError("The argument x must be in the range 0 < x <= 2")

    result = 0
    for k in range(1, terms + 1):
        result += calculate_term(x, k)

    return result


def print_taylor_formula(terms):
    formula = "ln(1+x) ≈ "
    for k in range(1, terms + 1):
        if k > 1:
            if k % 2 == 0:
                formula += " - "
            else:
                formula += " + "

        formula += f"x^{k}/{k}"

    print(formula)


def main():
    try:
        x_input = float(
            input("Enter the value of x to calculate ln(1+x) (0 < x <= 2): ")
        )

        if not (0 < x_input <= 2):
            print("Error: the value of x must be in the range 0 < x <= 2")
            return

        ln_3_terms = ln_taylor(x_input, 3)
        ln_4_terms = ln_taylor(x_input, 4)
        ln_5_terms = ln_taylor(x_input, 5)

        exact_ln = math.log(1 + x_input)

        print(f"\nResults of the calculation ln(1+{x_input}):")
        print(f"According to the Taylor formula (3 terms): {ln_3_terms}")
        print(f"According to the Taylor formula (4 terms): {ln_4_terms}")
        print(f"According to the Taylor formula (5 terms): {ln_5_terms}")
        print(f"The exact value (math.log): {exact_ln}")

        print("\nAbsolute errors:")
        print(f"For 3 terms: {abs(exact_ln - ln_3_terms)}")
        print(f"For 4 terms: {abs(exact_ln - ln_4_terms)}")
        print(f"For 5 terms: {abs(exact_ln - ln_5_terms)}")

        print("\nFormulas:")
        print("For 3 terms:", end=" ")
        print_taylor_formula(3)
        print("For 4 terms:", end=" ")
        print_taylor_formula(4)
        print("For 5 terms:", end=" ")
        print_taylor_formula(5)

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
