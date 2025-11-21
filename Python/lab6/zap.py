def sum(a, b):
    result = a + b
    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(f"The sum of {a} and {b} equals {result}\n")
    print(f"The sum of {a} and {b} equals {result}")

def main():
    try:
        a = int(input("Enter value a = "))
        b = int(input("Enter value b = "))
        sum(a, b)
        input("\nResult saved to result.txt\nPress Enter to exit")
    except ValueError:
        print("Error! Enter numeric values.")
        input("\nPress Enter to close the program")

if __name__ == "__main__":
    main()
