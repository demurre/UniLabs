from turtle import *

def draw_square(side_length):
    for _ in range(4):
        forward(side_length)
        left(90)

def move_to(x, y):
    up()
    goto(x, y)
    down()

draw_square(100)
move_to(150, 150)
draw_square(100)

done()