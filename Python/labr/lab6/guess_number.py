import turtle
import random


class NumberGuessingGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Guess the number")
        self.screen.bgcolor("#F5F5DC")
        self.screen.setup(700, 600)

        self.number_to_guess = random.randint(1, 100)
        self.current_input = ""
        self.attempts = 0
        self.last_guess = None

        self.setup_turtles()
        self.draw_interface()
        self.setup_click_handlers()

        self.message_turtle = turtle.Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.penup()
        self.message_turtle.goto(0, 30)

    def setup_turtles(self):
        self.title_turtle = turtle.Turtle()
        self.title_turtle.hideturtle()
        self.title_turtle.penup()
        self.title_turtle.goto(0, 200)

        self.button_turtle = turtle.Turtle()
        self.button_turtle.hideturtle()
        self.button_turtle.penup()
        self.button_turtle.speed(0)

        self.info_turtle = turtle.Turtle()
        self.info_turtle.hideturtle()
        self.info_turtle.penup()
        self.info_turtle.goto(0, 150)

        self.input_turtle = turtle.Turtle()
        self.input_turtle.hideturtle()
        self.input_turtle.penup()
        self.input_turtle.goto(0, 100)

    def draw_interface(self):
        self.title_turtle.write(
            "The computer has given you a number from 1 to 100. Enter your guess:",
            align="center",
            font=("Arial", 14, "italic"),
        )

        self.draw_buttons()

        self.update_display()

    def draw_buttons(self):
        positions = [
            [(-60, 0), (0, 0), (60, 0)],
            [(-60, -50), (0, -50), (60, -50)],
            [(-60, -100), (0, -100), (60, -100)],
            [(0, -150)],
        ]

        numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0]]

        self.buttons = {}

        for row_idx, (pos_row, num_row) in enumerate(zip(positions, numbers)):
            for pos, num in zip(pos_row, num_row):
                self.draw_button(pos[0], pos[1], str(num))
                self.buttons[str(num)] = pos

        self.draw_submit_button(0, -220)

    def draw_button(self, x, y, text):
        self.button_turtle.goto(x, y)
        self.button_turtle.setheading(0)

        self.button_turtle.pendown()
        self.button_turtle.pencolor("white")
        self.button_turtle.fillcolor("white")
        self.button_turtle.begin_fill()
        for _ in range(4):
            self.button_turtle.forward(40)
            self.button_turtle.left(90)
        self.button_turtle.end_fill()
        self.button_turtle.penup()

        self.button_turtle.goto(x + 20, y + 10)
        self.button_turtle.color("black")
        self.button_turtle.write(text, align="center", font=("Arial", 16, "bold"))

    def draw_submit_button(self, x, y):
        self.button_turtle.goto(x - 40, y)
        self.button_turtle.setheading(0)

        self.button_turtle.pendown()
        self.button_turtle.pencolor("#90EE90")
        self.button_turtle.fillcolor("#90EE90")
        self.button_turtle.begin_fill()
        self.button_turtle.forward(80)
        self.button_turtle.left(90)
        self.button_turtle.forward(30)
        self.button_turtle.left(90)
        self.button_turtle.forward(80)
        self.button_turtle.left(90)
        self.button_turtle.forward(30)
        self.button_turtle.left(90)
        self.button_turtle.end_fill()
        self.button_turtle.penup()

        self.button_turtle.goto(x, y + 12)
        self.button_turtle.color("black")
        self.button_turtle.write("Check", align="center", font=("Arial", 10, "bold"))

    def setup_click_handlers(self):
        self.screen.onclick(self.handle_click)

    def handle_click(self, x, y):
        for num, pos in self.buttons.items():
            if pos[0] <= x <= pos[0] + 40 and pos[1] <= y <= pos[1] + 40:
                self.add_digit(num)
                return

        if -40 <= x <= 40 and -220 <= y <= -190:
            self.submit_guess()

    def add_digit(self, digit):
        if len(self.current_input) < 3:
            self.current_input += digit
            self.update_display()

    def submit_guess(self):
        if not self.current_input:
            return

        guess = int(self.current_input)
        self.last_guess = guess
        self.attempts += 1
        self.current_input = ""

        if guess < self.number_to_guess:
            message = "Too little! Try again."
        elif guess > self.number_to_guess:
            message = "Too much! Try it out."
        else:
            message = (
                f"Congratulations! You guessed the number in {self.attempts} attempts!"
            )

        self.display_message(message)
        self.update_display()

    def update_display(self):
        self.input_turtle.clear()
        self.info_turtle.clear()

        if self.current_input:
            self.input_turtle.write(
                f"Your number: {self.current_input}",
                align="center",
                font=("Arial", 16, "bold"),
            )
        else:
            self.input_turtle.write(
                "Enter number...", align="center", font=("Arial", 12, "italic")
            )

        info_text = f"Number of attempts: {self.attempts}"
        if self.last_guess is not None:
            info_text += f" | The last guess: {self.last_guess}"

        self.info_turtle.goto(0, 70)
        self.info_turtle.write(info_text, align="center", font=("Arial", 12, "normal"))

    def display_message(self, message):
        self.message_turtle.clear()
        self.message_turtle.write(message, align="center", font=("Arial", 14, "bold"))

    def start_game(self):
        self.screen.listen()
        self.screen.mainloop()


game = NumberGuessingGame()
game.start_game()
