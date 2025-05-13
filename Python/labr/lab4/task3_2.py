def create_diagonal_array(n):
    array = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i + j == n - 1:
                array[i][j] = 1
            elif i + j > n - 1:
                array[i][j] = 2
            else:
                array[i][j] = 0

    return array


def print_array(array):
    for row in array:
        print(" ".join(map(str, row)))


n = int(input("Enter the size of the array n: "))

result = create_diagonal_array(n)
print_array(result)
