import random
import tkinter as tk
from tkinter import messagebox, simpledialog
import time


class YatzyGame:
    def __init__(self, master):
        self.master = master
        master.title("🎲 Yatzy (One dice)")
        master.geometry("500x600")
        master.configure(bg="lightyellow")

        self.target_score = None
        self.player_scores = [0, 0]
        self.current_player = 0
        self.rounds_played = 0
        self.delay_time = 1.0

        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(
            self.master,
            text="🎲 Yatzy",
            font=("Arial", 20, "bold"),
            bg="lightyellow",
        ).pack(pady=20)

        tk.Label(
            self.master,
            text="Choose a target number to win",
            font=("Arial", 14),
            bg="lightyellow",
        ).pack(pady=10)

        targets = [21, 30, 50, 60]
        for target in targets:
            btn = tk.Button(
                self.master,
                text=f"Target: {target}",
                command=lambda t=target: self.start_game(t),
                width=20,
                height=2,
            )
            btn.pack(pady=5)

        tk.Button(
            self.master,
            text="Exit",
            command=self.master.quit,
            width=20,
            height=2,
            bg="lightcoral",
        ).pack(pady=10)

    def start_game(self, target):
        self.target_score = target
        self.player_scores = [0, 0]
        self.current_player = 0
        self.rounds_played = 0

        self.setup_game_screen()

    def setup_game_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.info_label = tk.Label(
            self.master,
            text=f"Target number: {self.target_score}\nCurrent round: 0/5",
            font=("Arial", 14),
            bg="lightyellow",
        )
        self.info_label.pack(pady=10)

        self.score_label = tk.Label(
            self.master,
            text=f"Player 1: 0 | Player 2: 0",
            font=("Arial", 16),
            bg="lightyellow",
        )
        self.score_label.pack(pady=10)

        self.dice_label = tk.Label(
            self.master, text="🎲", font=("Arial", 100), bg="lightyellow"
        )
        self.dice_label.pack(pady=20)

        self.roll_button = tk.Button(
            self.master,
            text="Roll the dice",
            command=self.roll_dice,
            width=20,
            height=2,
        )
        self.roll_button.pack(pady=10)

        tk.Label(self.master, text="Delay time (sec):", bg="lightyellow").pack()
        self.delay_scale = tk.Scale(
            self.master,
            from_=0.5,
            to=3,
            resolution=0.5,
            orient=tk.HORIZONTAL,
            length=300,
            bg="lightyellow",
        )
        self.delay_scale.set(1.0)
        self.delay_scale.pack(pady=10)

        tk.Button(
            self.master,
            text="Exit",
            command=self.create_main_menu,
            width=20,
            height=2,
            bg="lightcoral",
        ).pack(pady=10)

    def roll_dice(self):
        self.roll_button.config(state=tk.DISABLED)

        dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        for _ in range(5):
            self.dice_label.config(text=random.choice(dice_faces))
            self.master.update()
            time.sleep(0.1)

        dice_value = random.randint(1, 6)
        self.dice_label.config(text=f"⚂{dice_value}")

        self.player_scores[self.current_player] += dice_value

        self.rounds_played += 1
        self.info_label.config(
            text=f"Target number: {self.target_score}\nCurrent round: {self.rounds_played}/5"
        )
        self.score_label.config(
            text=f"Player 1: {self.player_scores[0]} | Player 2: {self.player_scores[1]}"
        )

        self.current_player = 1 - self.current_player

        self.delay_time = self.delay_scale.get()

        if self.rounds_played >= 5:
            self.show_game_results()
        else:
            self.master.after(
                int(self.delay_time * 1000),
                lambda: self.roll_button.config(state=tk.NORMAL),
            )

    def show_game_results(self):
        winner = None
        if self.player_scores[0] >= self.target_score:
            winner = "Player 1"
        elif self.player_scores[1] >= self.target_score:
            winner = "Player 2"

        result_text = f"""
Results of the game:
Player 1: {self.player_scores[0]} points
Player 2: {self.player_scores[1]} points
Target number: {self.target_score}

{f"🏆 Winner: {winner}!" if winner else "🤝 Draw!"}
"""

        messagebox.showinfo("Results of the game", result_text)

        self.create_main_menu()


def main():
    root = tk.Tk()
    game = YatzyGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
