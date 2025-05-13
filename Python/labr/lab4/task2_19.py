array = [5, 3, 0, 8, 0, -2, 7, 0, 1, 0]

print("Initial array:")
print(array)

new_array = array.copy()

for i in range(len(array)):
    if array[i] == 0:
        if i >= 2:
            new_array[i] = array[i - 1] + array[i - 2]
            print(
                f"Replaced element with index {i}: 0 -> {new_array[i]} (sum {array[i-1]} and {array[i-2]})"
            )
        elif i == 1:
            new_array[i] = array[i - 1]
            print(
                f"Replaced element with index {i}: 0 -> {new_array[i]} (only one previous element {array[i-1]})"
            )
        else:
            print(f"Element with an index {i} remains zero (no previous elements)")

print("\nArray after replacing zeros:")
print(new_array)
