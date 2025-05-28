import random
import tkinter as tk
from tkinter import messagebox, ttk
import time


class YatzyGame:
    def __init__(self, master):
        self.master = master
        master.title("Yatzy - Five Dice Game")
        master.geometry("900x700")
        master.configure(bg="#F5F5DC")

        self.player_score = 0
        self.computer_score = 0
        self.round_number = 1
        self.total_rounds = 0
        self.dice_values = []
        self.computer_dice_values = []
        self.game_history = []
        self.player_wins = 0
        self.computer_wins = 0
        self.ties = 0

        self.setup_ui()

    def setup_ui(self):
        title_label = tk.Label(
            self.master,
            text="Yatzy - Five Dice Game",
            font=("Arial", 24, "bold"),
            bg="#F5F5DC",
            fg="#8B4513",
        )
        title_label.pack(pady=20)

        self.info_frame = tk.Frame(self.master, bg="#F5F5DC")
        self.info_frame.pack(fill="x", pady=10)

        self.round_label = tk.Label(
            self.info_frame,
            text=f"Round: {self.round_number}",
            font=("Arial", 16, "bold"),
            bg="#F5F5DC",
            fg="#2E8B57",
        )
        self.round_label.pack(side="left", padx=20)

        self.score_label = tk.Label(
            self.info_frame,
            text=f"Player: {self.player_score} | Computer: {self.computer_score}",
            font=("Arial", 16, "bold"),
            bg="#F5F5DC",
            fg="#B8860B",
        )
        self.score_label.pack(side="right", padx=20)

        self.stats_label = tk.Label(
            self.master,
            text=f"Wins: Player {self.player_wins} | Computer {self.computer_wins} | Ties {self.ties}",
            font=("Arial", 12),
            bg="#F5F5DC",
            fg="#4169E1",
        )
        self.stats_label.pack(pady=5)

        self.player_frame = tk.LabelFrame(
            self.master,
            text="Your Dice",
            font=("Arial", 14, "bold"),
            bg="#E6F3FF",
            fg="#1E90FF",
        )
        self.player_frame.pack(fill="x", padx=20, pady=10)

        self.player_dice_labels = []
        player_dice_frame = tk.Frame(self.player_frame, bg="#E6F3FF")
        player_dice_frame.pack(pady=10)

        for i in range(5):
            dice_label = tk.Label(
                player_dice_frame,
                text="*",
                font=("Arial", 40, "bold"),
                bg="#E6F3FF",
                relief="raised",
                bd=2,
                width=3,
                height=1,
            )
            dice_label.pack(side="left", padx=10)
            self.player_dice_labels.append(dice_label)

        self.player_result_label = tk.Label(
            self.player_frame,
            text="Click 'Roll Dice' to start",
            font=("Arial", 12, "bold"),
            bg="#E6F3FF",
            fg="#0000CD",
        )
        self.player_result_label.pack(pady=5)

        self.computer_frame = tk.LabelFrame(
            self.master,
            text="Computer's Dice",
            font=("Arial", 14, "bold"),
            bg="#FFE6E6",
            fg="#DC143C",
        )
        self.computer_frame.pack(fill="x", padx=20, pady=10)

        self.computer_dice_labels = []
        computer_dice_frame = tk.Frame(self.computer_frame, bg="#FFE6E6")
        computer_dice_frame.pack(pady=10)

        for i in range(5):
            dice_label = tk.Label(
                computer_dice_frame,
                text="*",
                font=("Arial", 40, "bold"),
                bg="#FFE6E6",
                relief="raised",
                bd=2,
                width=3,
                height=1,
            )
            dice_label.pack(side="left", padx=10)
            self.computer_dice_labels.append(dice_label)

        self.computer_result_label = tk.Label(
            self.computer_frame,
            text="Waiting for player's turn",
            font=("Arial", 12, "bold"),
            bg="#FFE6E6",
            fg="#8B0000",
        )
        self.computer_result_label.pack(pady=5)

        self.control_frame = tk.Frame(self.master, bg="#F5F5DC")
        self.control_frame.pack(pady=20)

        self.roll_button = tk.Button(
            self.control_frame,
            text="Roll Dice",
            command=self.roll_dice,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            width=18,
            height=2,
            relief="raised",
            bd=3,
        )
        self.roll_button.pack(side="left", padx=10)

        self.rules_button = tk.Button(
            self.control_frame,
            text="Game Rules",
            command=self.show_rules,
            font=("Arial", 14),
            bg="#2196F3",
            fg="white",
            width=15,
            height=2,
            relief="raised",
            bd=3,
        )
        self.rules_button.pack(side="left", padx=10)

        self.history_button = tk.Button(
            self.control_frame,
            text="Game History",
            command=self.show_history,
            font=("Arial", 14),
            bg="#FF9800",
            fg="white",
            width=15,
            height=2,
            relief="raised",
            bd=3,
        )
        self.history_button.pack(side="left", padx=10)

        self.quit_button = tk.Button(
            self.control_frame,
            text="Quit Game",
            command=self.quit_game,
            font=("Arial", 14),
            bg="#F44336",
            fg="white",
            width=15,
            height=2,
            relief="raised",
            bd=3,
        )
        self.quit_button.pack(side="left", padx=10)

        self.progress_frame = tk.Frame(self.master, bg="#F5F5DC")
        self.progress_frame.pack(pady=10)

        self.progress_var = tk.StringVar()
        self.progress_label = tk.Label(
            self.progress_frame,
            textvariable=self.progress_var,
            font=("Arial", 12),
            bg="#F5F5DC",
        )
        self.progress_label.pack()

    def show_rules(self):
        rules_text = """
YATZY GAME RULES

Game Objective: Score more points through dice combinations

Scoring system:
• Two of a kind → 5 points
• Three of a kind → 10 points  
• Four of a kind → 20 points
• Five of a kind (YATZY) → 50 points
• No combination → 0 points

Game rules:
1. You and the computer take turns rolling 5 dice
2. Points are awarded based on the combination
3. The game continues round by round
4. The winner is determined by the total score
5. In case of a tie, an additional round is offered

Good luck!
        """
        messagebox.showinfo("Yatzy Game Rules", rules_text)

    def show_history(self):
        if not self.game_history:
            messagebox.showinfo("Game History", "No complete games played yet.")
            return

        history_window = tk.Toplevel(self.master)
        history_window.title("Game History")
        history_window.geometry("500x400")
        history_window.configure(bg="#F5F5DC")

        tk.Label(
            history_window,
            text="Game History",
            font=("Arial", 16, "bold"),
            bg="#F5F5DC",
        ).pack(pady=10)

        text_frame = tk.Frame(history_window)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(
            text_frame, yscrollcommand=scrollbar.set, font=("Arial", 11), wrap="word"
        )
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        for i, game in enumerate(self.game_history, 1):
            text_widget.insert("end", f"Game #{i}:\n")
            text_widget.insert("end", f"Rounds played: {game['rounds']}\n")
            text_widget.insert(
                "end",
                f"Final score: Player {game['player_score']} - {game['computer_score']} Computer\n",
            )
            text_widget.insert("end", f"Winner: {game['winner']}\n")
            text_widget.insert("end", "-" * 40 + "\n\n")

        text_widget.config(state="disabled")

    def roll_dice(self):
        self.roll_button.config(state=tk.DISABLED)
        self.progress_var.set("Rolling your dice...")

        self.animate_dice_roll(self.player_dice_labels, "player")

        self.dice_values = [random.randint(1, 6) for _ in range(5)]
        player_points, player_combination = self.calculate_points(self.dice_values)

        self.update_dice_display(self.player_dice_labels, self.dice_values)
        self.player_result_label.config(
            text=f"Combination: {player_combination} | Points: {player_points}"
        )

        self.master.after(1500, lambda: self.computer_turn(player_points))

    def computer_turn(self, player_points):
        self.progress_var.set("Computer's turn...")

        self.animate_dice_roll(self.computer_dice_labels, "computer")

        self.computer_dice_values = [random.randint(1, 6) for _ in range(5)]
        computer_points, computer_combination = self.calculate_points(
            self.computer_dice_values
        )

        self.update_dice_display(self.computer_dice_labels, self.computer_dice_values)
        self.computer_result_label.config(
            text=f"Combination: {computer_combination} | Points: {computer_points}"
        )

        self.player_score += player_points
        self.computer_score += computer_points
        self.score_label.config(
            text=f"Player: {self.player_score} | Computer: {self.computer_score}"
        )

        self.progress_var.set("")
        self.check_round_results(player_points, computer_points)

    def animate_dice_roll(self, dice_labels, player_type):
        dice_symbols = ["1", "2", "3", "4", "5", "6"]
        animation_steps = 8 if player_type == "player" else 6

        for step in range(animation_steps):
            for label in dice_labels:
                if step % (random.randint(1, 2)) == 0:
                    label.config(text=random.choice(dice_symbols))
            self.master.update()
            time.sleep(0.15 if player_type == "player" else 0.1)

    def update_dice_display(self, dice_labels, values):
        for i, value in enumerate(values):
            dice_labels[i].config(text=str(value), relief="solid", bd=2)

    def calculate_points(self, dice_values):
        counts = {}
        for value in dice_values:
            counts[value] = counts.get(value, 0) + 1

        max_count = max(counts.values()) if counts else 0

        if max_count == 5:
            return 50, "YATZY! (5 of a kind)"
        elif max_count == 4:
            return 20, "4 of a kind"
        elif max_count == 3:
            return 10, "3 of a kind"
        elif max_count == 2:
            pairs_count = sum(1 for count in counts.values() if count == 2)
            if pairs_count == 2:
                return 5, "Two pairs"
            else:
                return 5, "One pair"
        else:
            return 0, "No combination"

    def check_round_results(self, player_points, computer_points):
        self.total_rounds += 1

        if player_points > computer_points:
            round_result = "You won this round!"
        elif computer_points > player_points:
            round_result = "Computer won this round!"
        else:
            round_result = "Tie in this round!"

        messagebox.showinfo(
            f"Round {self.round_number} Results",
            f"{round_result}\n\nYour points: {player_points}\nComputer's points: {computer_points}",
        )

        continue_game = messagebox.askyesno(
            "Continue Game", "Would you like to play another round?"
        )

        if continue_game:
            self.next_round()
        else:
            self.end_game()

    def next_round(self):
        self.round_number += 1
        self.round_label.config(text=f"Round: {self.round_number}")

        for label in self.player_dice_labels + self.computer_dice_labels:
            label.config(text="*", relief="raised", bd=2)

        self.player_result_label.config(text="Click 'Roll Dice' to continue")
        self.computer_result_label.config(text="Waiting for player's turn")

        self.roll_button.config(state=tk.NORMAL)
        self.progress_var.set("")

    def end_game(self):
        if self.player_score > self.computer_score:
            winner = "You won!"
            winner_text = "Player"
            self.player_wins += 1
        elif self.player_score < self.computer_score:
            winner = "Computer won!"
            winner_text = "Computer"
            self.computer_wins += 1
        else:
            winner = "Tie!"
            winner_text = "Tie"
            self.ties += 1

        self.game_history.append(
            {
                "rounds": self.total_rounds,
                "player_score": self.player_score,
                "computer_score": self.computer_score,
                "winner": winner_text,
            }
        )

        result_message = f"""
Game Over!

Game Statistics:
Rounds played: {self.total_rounds}

Final Score:
Player: {self.player_score} points
Computer: {self.computer_score} points

{winner}

Overall Statistics:
Player wins: {self.player_wins}
Computer wins: {self.computer_wins}
Ties: {self.ties}
        """

        messagebox.showinfo("Game Over", result_message)

        restart = messagebox.askyesno("New Game", "Would you like to start a new game?")
        if restart:
            self.reset_game()
        else:
            self.update_stats_display()

    def update_stats_display(self):
        self.stats_label.config(
            text=f"Wins: Player {self.player_wins} | Computer {self.computer_wins} | Ties {self.ties}"
        )

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.round_number = 1
        self.total_rounds = 0

        self.round_label.config(text=f"Round: {self.round_number}")
        self.score_label.config(
            text=f"Player: {self.player_score} | Computer: {self.computer_score}"
        )
        self.update_stats_display()

        for label in self.player_dice_labels + self.computer_dice_labels:
            label.config(text="*", relief="raised", bd=2)

        self.player_result_label.config(text="Click 'Roll Dice' to start")
        self.computer_result_label.config(text="Waiting for player's turn")

        self.roll_button.config(state=tk.NORMAL)
        self.progress_var.set("")

    def quit_game(self):
        if self.player_wins + self.computer_wins + self.ties > 0:
            final_stats = f"""
Final Session Statistics:

Games played: {len(self.game_history)}
Player wins: {self.player_wins}
Computer wins: {self.computer_wins}
Ties: {self.ties}

Thank you for playing!
            """
            messagebox.showinfo("Session Statistics", final_stats)

        result = messagebox.askyesno("Quit", "Are you sure you want to quit the game?")
        if result:
            self.master.destroy()


def main():
    root = tk.Tk()

    game = YatzyGame(root)

    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
