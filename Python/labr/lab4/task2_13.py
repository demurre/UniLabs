array = [10, 1, 8, 7, -3, 5, 6, 7]
print("Array:")
print(array)

negative_index = -1
for i in range(len(array)):
    if array[i] < 0:
        negative_index = i
        break

if negative_index == -1:
    print("\nThere are no negative elements in the array.")
elif negative_index == 0:
    print(
        "\nThe first element of the array is negative. There are no elements before it to check the sequence."
    )
else:
    print(f"\nElements before the first negative element ({array[negative_index]}):")
    sequence = array[:negative_index]
    print(sequence)

    is_decreasing = True
    for i in range(1, len(sequence)):
        if sequence[i] >= sequence[i - 1]:
            is_decreasing = False
            print(
                f"Violation of the decrease in positions {i-1} and {i}: {sequence[i-1]} and {sequence[i]}"
            )
            break

    if is_decreasing:
        print(
            "\nThe elements before the first negative element form a decreasing sequence."
        )
    else:
        print(
            "\nElements before the first negative element do NOT form a decreasing sequence."
        )
