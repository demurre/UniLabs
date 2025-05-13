array = [5, -3, 2, 7, -1, 0, 4, -8]

print("Initial array:")
print(array)

positive_count = 0
negative_count = 0

for num in array:
    if num > 0:
        positive_count += 1
    elif num < 0:
        negative_count += 1

print(f"\nNumber of positive elements: {positive_count}")
print(f"Number of negative elements: {negative_count}")

if positive_count == negative_count:
    print("\nThe number of positive and negative elements is already the same.")
else:
    if positive_count < negative_count:
        elements_to_add = negative_count - positive_count
        element_type = "positive"
        value_to_add = 1
    else:
        elements_to_add = positive_count - negative_count
        element_type = "negative"
        value_to_add = -1

    print(f"\nLacking {elements_to_add} {element_type} elements.")

    for _ in range(elements_to_add):
        array.append(value_to_add)

    print("\nArray after adding elements:")
    print(array)

    new_positive_count = 0
    new_negative_count = 0

    for num in array:
        if num > 0:
            new_positive_count += 1
        elif num < 0:
            new_negative_count += 1

    print(f"\nA new number of positive elements: {new_positive_count}")
    print(f"New number of negative elements: {new_negative_count}")

    if new_positive_count == new_negative_count:
        print("The number of positive and negative elements is now the same!")
