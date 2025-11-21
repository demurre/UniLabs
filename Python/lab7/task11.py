def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def find_gcd_of_list(numbers):
    current_gcd = numbers[0]
    for number in numbers[1:]:
        current_gcd = gcd(current_gcd, number)
    return current_gcd

numbers = [16, 32, 40, 64, 80, 128]
result = find_gcd_of_list(numbers)
print(f"Greatest common divisor: {result}")