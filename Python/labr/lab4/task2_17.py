array = [5, -3, 10, 0, 8, -1, 2, 4]

T = 100

print("Initial array:")
print(array)
print(f"Number T for distribution: {T}")

positive_elements = []
positive_indices = []
sum_positive = 0

for i, num in enumerate(array):
    if num > 0:
        positive_elements.append(num)
        positive_indices.append(i)
        sum_positive += num

if not positive_elements:
    print("\nThere are no positive elements in the array. Division is not possible.")
else:
    print(f"\nPositive elements: {positive_elements}")
    print(f"Sum of positive elements: {sum_positive}")

    shares = []
    for element in positive_elements:
        share = (element / sum_positive) * T
        shares.append(share)

    print("\nDistribution of shares:")
    for i, (element, share) in enumerate(zip(positive_elements, shares)):
        print(f"Element {element}: {share:.2f}")

    for i, share in zip(positive_indices, shares):
        array[i] += share

    print("\nArray after distribution:")
    print([round(x, 2) for x in array])

    total_distributed = sum(shares)
    print(f"\nTotal amount distributed: {total_distributed:.2f}")
    print(f"The difference with T: {abs(T - total_distributed):.10f}")
