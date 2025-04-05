x1, y1 = 2.5, -7.5
x2, y2 = 1.5, 0.4

if x2 - x1 != 0:
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1

    if b >= 0:
        print(f"y = {k}x + {b}")
    else:
        print(f"y = {k}x - {abs(b)}")
else:
    print(f"x = {x1}")
