import turtle
import random

def draw_triangle():
    size = random.randint(50, 150)
    color = random.choice(["red", "blue", "green", "yellow", "purple", "orange", "pink"])

    turtle.penup()
    turtle.goto(random.randint(-300, 300), random.randint(-300, 300))
    turtle.pendown()

    turtle.fillcolor(color)
    turtle.begin_fill()

    for _ in range(3):
        turtle.forward(size)
        turtle.left(120)

    turtle.end_fill()

def draw_random_triangles():
    turtle.speed(0)

    for _ in range(random.randint(5, 15)):
        draw_triangle()

    turtle.done()

draw_random_triangles()
