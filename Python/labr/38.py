import math


# y(x) = sqrt((9-2x)/(2x-21))
def calculate_function(x):
    try:
        under_root = (9 - 2 * x) / (2 * x - 21)
        if under_root < 0:
            return "Not defined"
        return math.sqrt(under_root)
    except ZeroDivisionError:
        return "Not defined (division by 0)"
    except ValueError:
        return "Not defined (negative root expression)"


start = 6.0
end = 9.0
step = 0.1

print(f"{'x':^10}|{'y(x)':^15}")
print("-" * 26)

steps = int((end - start) / step) + 1

for i in range(steps):
    x = start + i * step
    if x > end:
        break

    result = calculate_function(x)

    if isinstance(result, str):
        print(f"{x:^10.1f}|{result:^15}")
    else:
        print(f"{x:^10.1f}|{result:^15.6f}")
