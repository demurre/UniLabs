array = [9, 2, 6, 15, 8, 14, 3, 7, 10, 12]

print("Initial array:")
print(array)

divisible_by_3 = 0
for num in array:
    if num % 3 == 0:
        divisible_by_3 += 1

print(f"\nThe number of numbers divisible by 3 without a remainder: {divisible_by_3}")

even_numbers = []
for num in array:
    if num % 2 == 0:
        even_numbers.append(num)

if even_numbers:
    even_avg = sum(even_numbers) / len(even_numbers)
    print(f"Even numbers: {even_numbers}")
    print(f"Arithmetic mean of even numbers: {even_avg}")
else:
    even_avg = 0
    print("There are no even numbers in the array.")

new_array = [divisible_by_3] + array + [even_avg]

print("\nArray after adding calculated values:")
print(new_array)

print(f"\nThe size of the initial array: {len(array)}")
print(f"The size of the new array: {len(new_array)}")
print(
    f"The difference: {len(new_array) - len(array)} (array is increased by 2 elements)"
)

print("\nChecking the correct placement of calculated values:")
print(
    f"The first element of the new array (the number of numbers divisible by 3): {new_array[0]}"
)
print(
    f"The last element of the new array (arithmetic mean of even numbers): {new_array[-1]}"
)
