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


start = 9.0
end = 6.0
step = 0.1

print("{:^10}|{:^15}".format("x", "y(x)"))
print("-" * 26)

steps = int((start - end) / step) + 1

for i in range(steps):
    x = start - i * step
    if x < end:
        break

    result = calculate_function(x)

    if isinstance(result, str):
        print("{:^10.1f}|{:^15}".format(x, result))
    else:
        print("{:^10.1f}|{:^15.6f}".format(x, result))
