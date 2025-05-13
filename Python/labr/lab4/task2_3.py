array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
n = len(array)

print("Initial array:")
print(array)

for i in range(0, n - 1, 2):
    array[i], array[i + 1] = array[i + 1], array[i]

print("\nArray after swapping elements:")
print(array)
