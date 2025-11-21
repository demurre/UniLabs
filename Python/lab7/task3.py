def max_of_two(a,b):
    return a if a > b else b

def max_of_five(numbers):
    return max_of_two(max_of_two(max_of_two(numbers[0], numbers[1]), max_of_two(numbers[2], numbers[3])), numbers[4])

numbers = list(map(int, input("Enter five numbers separated by spaces: ").split()))

print("Largest number: ", max_of_five(numbers))