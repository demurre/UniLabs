def max_of_two(x, y):
    if x > y:
        return x
    else:
        return y

def find_max_of_five(numbers):
    max_num = numbers[0]
    for num in numbers[1:]:
        max_num = max_of_two(max_num, num)
    print(f"Largest number: {max_num}")

numbers = [1, 3, 9, 5, 2]
find_max_of_five(numbers)