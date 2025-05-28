import turtle
import random
import math

screen = turtle.Screen()
screen.title("Avoid the Enemy")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

player = turtle.Turtle()
player.shape("circle")
player.color("blue")
player.penup()
player.speed(0)
player.goto(0, 0)

enemy = turtle.Turtle()
enemy.shape("triangle")
enemy.color("red")
enemy.penup()
enemy.speed(0)
enemy.goto(random.randint(-390, 390), random.randint(-290, 290))

player_speed = 15
enemy_speed = 1.5

enemy_dx = random.choice([-1, 1]) * enemy_speed
enemy_dy = random.choice([-1, 1]) * enemy_speed

score = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-390, 260)


def move_up():
    y = player.ycor()
    if y < 280:
        player.sety(y + player_speed)


def move_down():
    y = player.ycor()
    if y > -280:
        player.sety(y - player_speed)


def move_left():
    x = player.xcor()
    if x > -380:
        player.setx(x - player_speed)


def move_right():
    x = player.xcor()
    if x < 380:
        player.setx(x + player_speed)


screen.listen()
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")


def is_collision(t1, t2):
    distance = math.sqrt(
        math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2)
    )
    return distance < 20


def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}", align="left", font=("Arial", 16, "normal"))


def game_over():
    score_display.goto(0, 0)
    score_display.write("GAME OVER!", align="center", font=("Arial", 24, "bold"))
    score_display.goto(0, -30)
    score_display.write(
        f"Final score: {score}", align="center", font=("Arial", 16, "normal")
    )
    score_display.goto(0, -60)
    score_display.write(
        "Press SPACE to restart", align="center", font=("Arial", 12, "normal")
    )


def restart_game():
    global score, enemy_dx, enemy_dy, game_running
    if not game_running:
        score = 0
        game_running = True
        player.goto(0, 0)
        enemy.goto(random.randint(-390, 390), random.randint(-290, 290))
        enemy_dx = random.choice([-1, 1]) * enemy_speed
        enemy_dy = random.choice([-1, 1]) * enemy_speed
        score_display.clear()
        score_display.goto(-390, 260)


game_running = True

screen.onkey(restart_game, "space")

while True:
    screen.update()

    if game_running:
        enemy.setx(enemy.xcor() + enemy_dx)
        enemy.sety(enemy.ycor() + enemy_dy)

        if enemy.xcor() > 380:
            enemy.setx(380)
            enemy_dx *= -1
        elif enemy.xcor() < -380:
            enemy.setx(-380)
            enemy_dx *= -1

        if enemy.ycor() > 280:
            enemy.sety(280)
            enemy_dy *= -1
        elif enemy.ycor() < -280:
            enemy.sety(-280)
            enemy_dy *= -1

        score += 1
        update_score()

        if is_collision(player, enemy):
            game_running = False
            game_over()

        if score % 2000 == 0 and score > 0:
            if abs(enemy_dx) < 4:
                enemy_dx *= 1.05
                enemy_dy *= 1.05

    screen.delay(20)

screen.exitonclick()
