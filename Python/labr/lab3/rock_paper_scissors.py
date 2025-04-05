import random
import tkinter as tk
from tkinter import messagebox, simpledialog


class RockPaperScissorsGame:
    def __init__(self, master):
        self.master = master
        master.title("Rock, scissors, paper")
        master.geometry("500x400")
        master.configure(bg="#F5F5DC")

        self.total_games = 1
        self.current_game = 0
        self.player_wins = 0
        self.computer_wins = 0
        self.draws = 0

        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(
            self.master, text="Select the game mode", font=("Arial", 16), bg="#F5F5DC"
        ).pack(pady=20)

        tk.Button(
            self.master,
            text="One game",
            command=lambda: self.start_game(1),
            width=20,
            height=2,
        ).pack(pady=10)

        tk.Button(
            self.master,
            text="Series of games",
            command=self.get_game_count,
            width=20,
            height=2,
        ).pack(pady=10)

    def get_game_count(self):
        try:
            self.total_games = simpledialog.askinteger(
                "Number of games", "Enter the number of games:", minvalue=1, maxvalue=10
            )
            if self.total_games:
                self.start_game(self.total_games)
        except Exception:
            messagebox.showerror("Error", "Incorrect number of games")

    def start_game(self, total_games):
        self.total_games = total_games
        self.current_game = 0
        self.player_wins = 0
        self.computer_wins = 0
        self.draws = 0

        self.game_window()

    def game_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(
            self.master,
            text=f"Game {self.current_game + 1}/{self.total_games}",
            font=("Arial", 14),
            bg="#F5F5DC",
        ).pack(pady=10)

        self.result_label = tk.Label(
            self.master, text="", font=("Arial", 12), bg="#F5F5DC"
        )
        self.result_label.pack(pady=10)

        buttons_frame = tk.Frame(self.master, bg="#F5F5DC")
        buttons_frame.pack(pady=20)

        choices = [("Rock", "rock"), ("Scissors", "scissors"), ("Paper", "paper")]

        for text, choice in choices:
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=lambda c=choice: self.play_round(c),
                width=15,
                height=3,
            )
            btn.pack(side=tk.LEFT, padx=10)

    def play_round(self, player_choice):
        choices = ["rock", "scissors", "paper"]
        computer_choice = random.choice(choices)

        result = self.determine_winner(player_choice, computer_choice)

        if result == "Player's win":
            self.player_wins += 1
        elif result == "Computer's win":
            self.computer_wins += 1
        else:
            self.draws += 1

        self.result_label.config(
            text=f"You: {player_choice.capitalize()}, Computer: {computer_choice.capitalize()}\n{result}"
        )

        self.current_game += 1

        if self.current_game >= self.total_games:
            self.show_final_results()

    def determine_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            return "Draw"

        win_combinations = {"rock": "scissors", "scissors": "paper", "paper": "rock"}

        if win_combinations.get(player_choice) == computer_choice:
            return "Player's win"
        else:
            return "Computer's win"

    def show_final_results(self):
        result_text = f"""
        Game results:
        Your wins: {self.player_wins}
        Computer wins: {self.computer_wins}
        Draws: {self.draws}
        """

        if self.player_wins > self.computer_wins:
            result_text += "\nYou win!"
        elif self.player_wins < self.computer_wins:
            result_text += "\nComputer win!"
        else:
            result_text += "\nDraw!"

        messagebox.showinfo("Results", result_text)
        self.create_main_menu()


def main():
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
