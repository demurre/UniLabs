import turtle
import random


def draw_triangle(t, size, fill_color):
    t.fillcolor(fill_color)
    t.begin_fill()
    for _ in range(3):
        t.forward(size)
        t.left(120)
    t.end_fill()


def draw_square(t, size, fill_color):

    t.fillcolor(fill_color)
    t.begin_fill()
    for _ in range(4):
        t.forward(size)
        t.left(90)
    t.end_fill()


def get_random_color():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)


def get_random_position(screen_width, screen_height):
    x = random.randint(-screen_width // 2 + 50, screen_width // 2 - 50)
    y = random.randint(-screen_height // 2 + 50, screen_height // 2 - 50)
    return (x, y)


def create_graphics_field():
    screen = turtle.Screen()
    screen.title("Random triangles and squares")
    screen.bgcolor("white")

    screen_width = 800
    screen_height = 600
    screen.setup(width=screen_width, height=screen_height)

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()

    num_triangles = random.randint(3, 7)
    num_squares = random.randint(3, 7)

    for _ in range(num_triangles):
        size = random.randint(30, 100)
        color = get_random_color()
        position = get_random_position(screen_width, screen_height)

        t.penup()
        t.goto(position)
        t.pendown()

        draw_triangle(t, size, color)

    for _ in range(num_squares):
        size = random.randint(30, 100)
        color = get_random_color()
        position = get_random_position(screen_width, screen_height)

        t.penup()
        t.goto(position)
        t.pendown()

        draw_square(t, size, color)

    t.penup()
    t.goto(-screen_width // 2 + 20, screen_height // 2 - 40)
    t.pencolor("black")
    t.write(
        f"Triangles: {num_triangles}, Squares: {num_squares}",
        font=("Arial", 12, "normal"),
    )

    screen.exitonclick()


if __name__ == "__main__":
    create_graphics_field()
