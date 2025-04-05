import random
import math
import tkinter as tk
from tkinter import messagebox


class GuessNumberGame:
    def __init__(self, master):
        self.master = master
        master.title("Game 'Guess the number'")
        master.geometry("400x300")
        master.configure(bg="#F5F5DC")

        self.difficulty_levels = {
            1: (0, 10, "Easy"),
            2: (20, 60, "Medium"),
            3: (1, 100, "Hard"),
        }

        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(
            self.master,
            text="Choose the level of difficulty",
            font=("Arial", 16),
            bg="#F5F5DC",
        ).pack(pady=20)

        for level, (_, _, name) in self.difficulty_levels.items():
            btn = tk.Button(
                self.master,
                text=name,
                command=lambda l=level: self.start_game(l),
                width=20,
                height=2,
            )
            btn.pack(pady=10)

    def start_game(self, level):
        game_range = self.difficulty_levels[level][:2]
        level_name = self.difficulty_levels[level][2]

        secret_number = random.randint(game_range[0], game_range[1])
        max_attempts = math.ceil(math.log2(game_range[1] - game_range[0] + 1)) + 1

        self.game_window(secret_number, game_range, max_attempts, level_name)

    def game_window(self, secret_number, game_range, max_attempts, level_name):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.secret_number = secret_number
        self.game_range = game_range
        self.max_attempts = max_attempts
        self.current_attempt = 0

        tk.Label(
            self.master,
            text=f"Level: {level_name}",
            font=("Arial", 14),
            bg="#F5F5DC",
        ).pack(pady=10)
        tk.Label(
            self.master,
            text=f"A number in the range {game_range[0]}-{game_range[1]}",
            font=("Arial", 12),
            bg="#F5F5DC",
        ).pack()

        self.result_label = tk.Label(
            self.master, text="", font=("Arial", 12), bg="#F5F5DC"
        )
        self.result_label.pack(pady=10)

        self.guess_entry = tk.Entry(self.master, font=("Arial", 14), width=10)
        self.guess_entry.pack(pady=10)
        self.guess_entry.focus()

        tk.Button(self.master, text="Check", command=self.check_guess).pack(pady=10)

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.current_attempt += 1

            if guess < self.game_range[0] or guess > self.game_range[1]:
                self.result_label.config(
                    text=f"The number must be in the range {self.game_range[0]}-{self.game_range[1]}",
                    fg="red",
                )
                return

            if guess == self.secret_number:
                messagebox.showinfo(
                    "Win!",
                    f"You guessed the number {self.secret_number} in {self.current_attempt} tries!",
                )
                self.create_main_menu()
            elif self.current_attempt == self.max_attempts:
                messagebox.showinfo(
                    "Game over",
                    f"Unfortunately, you were wrong. The number was {self.secret_number}",
                )
                self.create_main_menu()
            else:
                if guess < self.secret_number:
                    self.result_label.config(text="The number is greater", fg="blue")
                else:
                    self.result_label.config(text="The number is smaller", fg="blue")

            self.guess_entry.delete(0, tk.END)

        except ValueError:
            self.result_label.config(text="Enter the correct number", fg="red")


def main():
    root = tk.Tk()
    game = GuessNumberGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
