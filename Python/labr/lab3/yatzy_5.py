import random
import tkinter as tk
from tkinter import messagebox
import time


class YatzyGame:
    def __init__(self, master):
        self.master = master
        master.title("🎲 Yatzy - The game with five dice")
        master.geometry("800x600")
        master.configure(bg="#F5F5DC")

        self.player_score = 0
        self.computer_score = 0
        self.round_number = 1
        self.dice_values = []
        self.computer_dice_values = []

        self.setup_ui()

    def setup_ui(self):
        title_label = tk.Label(
            self.master,
            text="🎲 Yatzy - The game with five dice 🎲",
            font=("Arial", 24, "bold"),
            bg="#F5F5DC",
        )
        title_label.pack(pady=20)

        self.info_frame = tk.Frame(self.master, bg="#F5F5DC")
        self.info_frame.pack(fill="x", pady=10)

        self.round_label = tk.Label(
            self.info_frame,
            text=f"Round: {self.round_number}",
            font=("Arial", 14),
            bg="#F5F5DC",
        )
        self.round_label.pack(side="left", padx=20)

        self.score_label = tk.Label(
            self.info_frame,
            text=f"Player: {self.player_score} | Computer: {self.computer_score}",
            font=("Arial", 14),
            bg="#F5F5DC",
        )
        self.score_label.pack(side="right", padx=20)

        self.player_frame = tk.LabelFrame(
            self.master, text="Your dice", font=("Arial", 14), bg="#F5F5DC"
        )
        self.player_frame.pack(fill="x", padx=20, pady=10)

        self.player_dice_labels = []
        player_dice_frame = tk.Frame(self.player_frame, bg="#F5F5DC")
        player_dice_frame.pack(pady=10)

        for i in range(5):
            dice_label = tk.Label(
                player_dice_frame, text="🎲", font=("Arial", 40), bg="#F5F5DC"
            )
            dice_label.pack(side="left", padx=10)
            self.player_dice_labels.append(dice_label)

        self.player_result_label = tk.Label(
            self.player_frame, text="", font=("Arial", 12), bg="#F5F5DC"
        )
        self.player_result_label.pack(pady=5)

        self.computer_frame = tk.LabelFrame(
            self.master, text="Computer's dice", font=("Arial", 14), bg="#F5F5DC"
        )
        self.computer_frame.pack(fill="x", padx=20, pady=10)

        self.computer_dice_labels = []
        computer_dice_frame = tk.Frame(self.computer_frame, bg="#F5F5DC")
        computer_dice_frame.pack(pady=10)

        for i in range(5):
            dice_label = tk.Label(
                computer_dice_frame, text="🎲", font=("Arial", 40), bg="#F5F5DC"
            )
            dice_label.pack(side="left", padx=10)
            self.computer_dice_labels.append(dice_label)

        self.computer_result_label = tk.Label(
            self.computer_frame, text="", font=("Arial", 12), bg="#F5F5DC"
        )
        self.computer_result_label.pack(pady=5)

        self.control_frame = tk.Frame(self.master, bg="#F5F5DC")
        self.control_frame.pack(pady=20)

        self.roll_button = tk.Button(
            self.control_frame,
            text="Roll the dice",
            command=self.roll_dice,
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white",
            width=15,
        )
        self.roll_button.pack(side="left", padx=10)

        self.quit_button = tk.Button(
            self.control_frame,
            text="Exit",
            command=self.quit_game,
            font=("Arial", 14),
            bg="#F44336",
            fg="white",
            width=15,
        )
        self.quit_button.pack(side="left", padx=10)

    def roll_dice(self):
        self.roll_button.config(state=tk.DISABLED)

        self.animate_dice_roll(self.player_dice_labels)

        self.dice_values = [random.randint(1, 6) for _ in range(5)]
        player_points, player_combination = self.calculate_points(self.dice_values)

        self.update_dice_display(self.player_dice_labels, self.dice_values)
        self.player_result_label.config(
            text=f"Combination: {player_combination} | Points: {player_points}"
        )

        self.master.after(1000, lambda: self.computer_turn(player_points))

    def computer_turn(self, player_points):
        self.animate_dice_roll(self.computer_dice_labels)

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

        self.check_round_results(player_points, computer_points)

    def animate_dice_roll(self, dice_labels):
        dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

        for _ in range(5):
            for label in dice_labels:
                label.config(text=random.choice(dice_faces))
            self.master.update()
            time.sleep(0.1)

    def update_dice_display(self, dice_labels, values):
        dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        for i, value in enumerate(values):
            dice_labels[i].config(text=dice_faces[value - 1])

    def calculate_points(self, dice_values):
        counts = {i: dice_values.count(i) for i in range(1, 7)}
        max_count = max(counts.values()) if counts else 0

        if max_count == 5:
            return 50, "Yatzy"
        elif max_count == 4:
            return 20, "Four are the same"
        elif max_count == 3:
            return 10, "Three are the same"
        elif max_count == 2:
            pairs = sum(1 for count in counts.values() if count == 2)
            if pairs == 2:
                return 5, "Two are the same"
            else:
                return 5, "Two are the same"
        else:
            return 0, "No combination"

    def check_round_results(self, player_points, computer_points):
        if self.player_score > self.computer_score and player_points > 0:
            self.show_round_result("You are in the lead!")
        elif self.computer_score > self.player_score and computer_points > 0:
            self.show_round_result("Computer is in the lead!")
        elif player_points == computer_points and player_points > 0:
            self.show_round_result("Draw in this round!")
        else:
            self.show_round_result("No one scored points in this round.")

        if self.player_score == self.computer_score:
            message = "Draw! An additional round is required."
            result = messagebox.askyesno(
                "Draw", "Draw! Would you like to play an additional round?"
            )
            if result:
                self.next_round()
            else:
                self.quit_game()
        else:
            result = messagebox.askyesno(
                "Next round", "Would you like to play another round?"
            )
            if result:
                self.next_round()
            else:
                self.end_game()

    def show_round_result(self, message):
        self.roll_button.config(state=tk.NORMAL)
        messagebox.showinfo(f"Round result {self.round_number}", message)

    def next_round(self):
        self.round_number += 1
        self.round_label.config(text=f"Round: {self.round_number}")

        for label in self.player_dice_labels + self.computer_dice_labels:
            label.config(text="🎲")

        self.player_result_label.config(text="")
        self.computer_result_label.config(text="")

        self.roll_button.config(state=tk.NORMAL)

    def end_game(self):
        if self.player_score > self.computer_score:
            winner = "You won!"
        elif self.player_score < self.computer_score:
            winner = "Computer won!"
        else:
            winner = "Draw!"

        result_message = f"""
        The game is over!!
        
        Total score:
        Player: {self.player_score}
        Computer: {self.computer_score}
        
        {winner}
        """

        messagebox.showinfo("Game over", result_message)

        restart = messagebox.askyesno("New game", "Want to start a new game?")
        if restart:
            self.reset_game()
        else:
            self.quit_game()

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.round_number = 1

        self.round_label.config(text=f"Round: {self.round_number}")
        self.score_label.config(
            text=f"Player: {self.player_score} | Computer: {self.computer_score}"
        )

        for label in self.player_dice_labels + self.computer_dice_labels:
            label.config(text="🎲")

        self.player_result_label.config(text="")
        self.computer_result_label.config(text="")

        self.roll_button.config(state=tk.NORMAL)

    def quit_game(self):
        result = messagebox.askyesno("Exit", "Are you sure you want to leave?")
        if result:
            self.master.destroy()


def main():
    root = tk.Tk()
    game = YatzyGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
