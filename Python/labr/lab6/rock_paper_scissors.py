import turtle
import random


class RockPaperScissorsGame:
    def __init__(self):
        self.wn = turtle.Screen()
        self.wn.title("Rock, scissors, paper")
        self.wn.bgcolor("#E6F3FF")
        self.wn.setup(800, 700)

        self.options = ["rock", "scissors", "paper"]
        self.symbols = {"rock": "●", "scissors": "✂", "paper": "▢"}
        self.user_score = 0
        self.comp_score = 0
        self.total_games = 0
        self.max_games = 5
        self.game_active = True

        self.setup_turtles()
        self.draw_interface()
        self.setup_game_controls()

    def setup_turtles(self):
        self.title_turtle = turtle.Turtle()
        self.title_turtle.hideturtle()
        self.title_turtle.penup()
        self.title_turtle.goto(0, 280)
        self.title_turtle.color("#2E4057")

        self.score_turtle = turtle.Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.goto(0, 240)
        self.score_turtle.color("#FF6B35")

        self.progress_turtle = turtle.Turtle()
        self.progress_turtle.hideturtle()
        self.progress_turtle.penup()
        self.progress_turtle.goto(0, 200)
        self.progress_turtle.color("#4A90A4")

        self.result_turtle = turtle.Turtle()
        self.result_turtle.hideturtle()
        self.result_turtle.penup()
        self.result_turtle.goto(0, 120)
        self.result_turtle.color("#2E4057")

        self.choice_turtle = turtle.Turtle()
        self.choice_turtle.hideturtle()
        self.choice_turtle.penup()
        self.choice_turtle.goto(0, 60)
        self.choice_turtle.color("#5A5A5A")

        self.winner_turtle = turtle.Turtle()
        self.winner_turtle.hideturtle()
        self.winner_turtle.penup()
        self.winner_turtle.goto(0, -50)
        self.winner_turtle.color("#FF1744")

        self.button_turtle = turtle.Turtle()
        self.button_turtle.hideturtle()
        self.button_turtle.penup()
        self.button_turtle.speed(0)

    def draw_interface(self):
        self.title_turtle.write(
            "ROCK, PAPER, SCISSORS", align="center", font=("Arial", 20, "bold")
        )

        self.draw_choice_buttons()

        self.draw_settings_buttons()

        self.update_display()

    def draw_choice_buttons(self):
        positions = [(-200, -120), (0, -120), (200, -120)]
        colors = ["#FFE082", "#A5D6A7", "#FFAB91"]

        self.choice_buttons = {}

        for i, (choice, pos, color) in enumerate(zip(self.options, positions, colors)):
            x, y = pos

            self.draw_round_button(x, y, color, choice)
            self.choice_buttons[choice] = (x, y)

            self.button_turtle.goto(x, y + 15)
            self.button_turtle.color("black")
            self.button_turtle.write(
                self.symbols[choice], align="center", font=("Arial", 24, "bold")
            )

            self.button_turtle.goto(x, y - 25)
            self.button_turtle.write(
                choice.upper(), align="center", font=("Arial", 12, "bold")
            )

    def draw_settings_buttons(self):
        settings_y = -220

        self.draw_small_button(-100, settings_y, "#FF8A80", "-")

        self.games_turtle = turtle.Turtle()
        self.games_turtle.hideturtle()
        self.games_turtle.penup()
        self.games_turtle.goto(0, settings_y - 5)
        self.games_turtle.color("#2E4057")

        self.draw_small_button(100, settings_y, "#80C784", "+")

        self.draw_reset_button(0, -280)

    def draw_round_button(self, x, y, color, choice):
        self.button_turtle.goto(x, y - 40)
        self.button_turtle.setheading(0)
        self.button_turtle.pendown()
        self.button_turtle.fillcolor(color)
        self.button_turtle.pencolor(color)
        self.button_turtle.begin_fill()
        self.button_turtle.circle(40)
        self.button_turtle.end_fill()
        self.button_turtle.penup()

    def draw_small_button(self, x, y, color, text):
        self.button_turtle.goto(x - 15, y - 15)
        self.button_turtle.setheading(0)
        self.button_turtle.pendown()
        self.button_turtle.fillcolor(color)
        self.button_turtle.pencolor(color)
        self.button_turtle.begin_fill()
        for _ in range(4):
            self.button_turtle.forward(30)
            self.button_turtle.left(90)
        self.button_turtle.end_fill()
        self.button_turtle.penup()

        self.button_turtle.goto(x, y - 5)
        self.button_turtle.color("black")
        self.button_turtle.write(text, align="center", font=("Arial", 16, "bold"))

    def draw_reset_button(self, x, y):
        self.button_turtle.goto(x - 40, y - 15)
        self.button_turtle.setheading(0)
        self.button_turtle.pendown()
        self.button_turtle.fillcolor("#E1BEE7")
        self.button_turtle.pencolor("#E1BEE7")
        self.button_turtle.begin_fill()
        for _ in range(4):
            self.button_turtle.forward(80)
            self.button_turtle.left(90)
        self.button_turtle.end_fill()
        self.button_turtle.penup()

        self.button_turtle.goto(x, y - 5)
        self.button_turtle.color("black")
        self.button_turtle.write("NEW GAME", align="center", font=("Arial", 10, "bold"))

    def setup_game_controls(self):
        self.wn.onclick(self.handle_click)

    def handle_click(self, x, y):
        if self.game_active:
            for choice, pos in self.choice_buttons.items():
                btn_x, btn_y = pos
                if btn_x - 40 <= x <= btn_x + 40 and btn_y - 40 <= y <= btn_y + 40:
                    self.play(choice)
                    return

        if -115 <= x <= -85 and -235 <= y <= -205:
            if self.max_games > 1:
                self.max_games -= 1
                self.update_display()

        elif 85 <= x <= 115 and -235 <= y <= -205:
            if self.max_games < 20:
                self.max_games += 1
                self.update_display()

        elif -40 <= x <= 40 and -295 <= y <= -265:
            self.reset_game()

    def play(self, user_choice):
        if self.total_games >= self.max_games:
            return

        comp_choice = random.choice(self.options)
        result = self.determine_winner(user_choice, comp_choice)

        self.total_games += 1

        if "You win" in result:
            self.user_score += 1
        elif "Computer wins" in result:
            self.comp_score += 1

        self.show_round_result(user_choice, comp_choice, result)

        if self.total_games >= self.max_games:
            self.end_game()

    def determine_winner(self, user, comp):
        if user == comp:
            return "Tie!"
        elif (
            (user == "rock" and comp == "scissors")
            or (user == "scissors" and comp == "paper")
            or (user == "paper" and comp == "rock")
        ):
            return "You win the round!"
        else:
            return "Computer wins the round!"

    def show_round_result(self, user_choice, comp_choice, result):
        self.choice_turtle.clear()
        self.result_turtle.clear()

        choice_text = (
            f"You: {self.symbols[user_choice]} {user_choice.upper()}     "
            f"Computer: {self.symbols[comp_choice]} {comp_choice.upper()}"
        )
        self.choice_turtle.write(
            choice_text, align="center", font=("Arial", 14, "normal")
        )

        self.result_turtle.write(result, align="center", font=("Arial", 16, "bold"))

        self.update_display()

    def update_display(self):
        self.score_turtle.clear()
        score_text = f"Score - You: {self.user_score} | Computer: {self.comp_score}"
        self.score_turtle.write(score_text, align="center", font=("Arial", 16, "bold"))

        self.progress_turtle.clear()
        progress_text = f"Round {self.total_games}/{self.max_games}"
        self.progress_turtle.write(
            progress_text, align="center", font=("Arial", 12, "normal")
        )

        self.games_turtle.clear()
        games_text = f"Play to {self.max_games}"
        self.games_turtle.write(
            games_text, align="center", font=("Arial", 10, "normal")
        )

    def end_game(self):
        self.game_active = False
        self.winner_turtle.clear()

        if self.user_score > self.comp_score:
            winner_text = f"VICTORY!\nYou won {self.user_score}:{self.comp_score}!"
            self.winner_turtle.color("#4CAF50")
        elif self.comp_score > self.user_score:
            winner_text = f"DEFEAT\nComputer won {self.comp_score}:{self.user_score}!"
            self.winner_turtle.color("#F44336")
        else:
            winner_text = f"DRAW!\nFinal score {self.user_score}:{self.comp_score}!"
            self.winner_turtle.color("#FF9800")

        self.winner_turtle.write(
            winner_text, align="center", font=("Arial", 18, "bold")
        )

    def reset_game(self):
        self.user_score = 0
        self.comp_score = 0
        self.total_games = 0
        self.game_active = True

        self.choice_turtle.clear()
        self.result_turtle.clear()
        self.winner_turtle.clear()

        self.update_display()

    def start_game(self):
        self.wn.listen()
        self.wn.mainloop()


game = RockPaperScissorsGame()
game.start_game()
