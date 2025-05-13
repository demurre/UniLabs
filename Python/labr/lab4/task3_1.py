n = 5
m = 8

print(f"Create a checkerboard pattern with a size {n}×{m}")

chessboard = []
for i in range(n):
    row = []
    for j in range(m):
        if (i + j) % 2 == 0:
            row.append(".")
        else:
            row.append("*")
    chessboard.append(row)

print("\nResult:")
for row in chessboard:
    print("".join(row))

print("\nVerification:")
print(f"The symbol in the upper left corner: {chessboard[0][0]}")
