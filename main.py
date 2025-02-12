import random
import tkinter as tk
from tkinter import ttk, messagebox, font
from tkinter.scrolledtext import ScrolledText
import winsound


class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🔢 Mystery Number Hunter")
        self.root.geometry("600x700")
        self.root.configure(bg="#2E2E2E")
        self.root.resizable(False, False)

        self.max_attempts = 10
        self.attempts = 0
        self.secret_number = 0
        self.max_score = 1000
        self.current_score = 0
        self.game_active = False
        self.hint_count = 0
        self.guess_history = []

        self.colors = {
            "bg": "#2E2E2E",
            "fg": "#FFFFFF",
            "accent": "#4CAF50",
            "warning": "#FF5252",
            "highlight": "#2196F3"
        }

        self.custom_font = font.Font(family="Helvetica", size=12)
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")

        self.create_widgets()
        self.setup_bindings()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title_label = ttk.Label(
            main_frame,
            text="🔍 Mystery Number Hunter",
            font=self.title_font,
            foreground=self.colors["accent"],
            background=self.colors["bg"]
        )
        title_label.pack(pady=15)

        level_frame = ttk.LabelFrame(main_frame, text="Select Difficulty Level")
        level_frame.pack(pady=10, fill="x")
        self.style = ttk.Style()

        self.style.configure("Beginner.TButton", foreground="black", background="#4CAF50")
        self.style.configure("Casual.TButton", foreground="black", background="#2196F3")
        self.style.configure("Pro.TButton", foreground="black", background="#FF9800")
        self.style.configure("Expert.TButton", foreground="black", background="#F44336")
        levels = {
            "😊 Beginner (12 attempts)": (12, "Beginner.TButton"),
            "😎 Casual (9 attempts)": (9, "Casual.TButton"),
            "🔥 Pro (6 attempts)": (6, "Pro.TButton"),
            "💀 Expert (3 attempts)": (3, "Expert.TButton")
        }

        for level, (attempts, style_name) in levels.items():
            btn = ttk.Button(
                level_frame,
                text=level,
                command=lambda a=attempts: self.set_level(a),
                style=style_name
            )
            btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        self.status_label = ttk.Label(
            main_frame,
            text="Select a difficulty level to start!",
            foreground=self.colors["fg"],
            background=self.colors["bg"],
            font=self.custom_font
        )
        self.status_label.pack(pady=10)

        self.progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            mode="determinate",
            length=400
        )
        self.progress.pack(pady=5)

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10)

        self.guess_entry = ttk.Entry(
            input_frame,
            font=self.custom_font,
            width=15,
            state="disabled"
        )
        self.guess_entry.pack(side="left", padx=5)

        self.submit_btn = ttk.Button(
            input_frame,
            text="Submit Guess",
            command=self.check_guess,
            state="disabled",
            style="Accent.TButton"
        )
        self.submit_btn.pack(side="left")

        history_frame = ttk.LabelFrame(main_frame, text="Guess History")
        history_frame.pack(pady=10, fill="both", expand=True)

        self.history_display = ScrolledText(
            history_frame,
            height=8,
            wrap=tk.WORD,
            font=self.custom_font,
            bg="#333333",
            fg="white",
            insertbackground="white"
        )
        self.history_display.pack(padx=5, pady=5, fill="both", expand=True)
        self.history_display.configure(state="disabled")

        self.hint_label = ttk.Label(
            main_frame,
            text="",
            foreground=self.colors["highlight"],
            background=self.colors["bg"],
            font=self.custom_font
        )
        self.hint_label.pack(pady=5)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=10)

        self.reset_btn = ttk.Button(
            control_frame,
            text="🔄 New Game",
            command=self.reset_game,
            state="disabled"
        )
        self.reset_btn.pack(side="left", padx=5)

        ttk.Button(
            control_frame,
            text="ℹ️ Help",
            command=self.show_help
        ).pack(side="left", padx=5)

        self.score_label = ttk.Label(
            main_frame,
            text=f"Score: {self.current_score}",
            foreground=self.colors["accent"],
            background=self.colors["bg"],
            font=self.custom_font
        )
        self.score_label.pack(pady=5)

        self.style = ttk.Style()
        self.style.configure("Accent.TButton", foreground="white", background="#4CAF50")
        self.style.map("Accent.TButton", background=[("active", "#45a049")])

    def setup_bindings(self):
        self.root.bind("<Return>", lambda event: self.check_guess())
        self.guess_entry.bind("<FocusIn>", lambda event: self.guess_entry.select_range(0, tk.END))

    def set_level(self, attempts):
        self.max_attempts = attempts
        self.attempts = 0
        self.current_score = 1000
        self.secret_number = random.randint(1, 100)
        self.game_active = True
        self.hint_count = 0
        self.guess_history = []

        self.update_display(f"Game started! You have {self.max_attempts} attempts")
        self.progress["maximum"] = self.max_attempts
        self.progress["value"] = 0
        self.guess_entry.config(state="normal")
        self.submit_btn.config(state="normal")
        self.reset_btn.config(state="normal")
        self.hint_label.config(text="")
        self.update_score()
        self.clear_history()
        self.guess_entry.focus()

    def check_guess(self):
        if not self.game_active:
            return

        guess = self.guess_entry.get()
        if not guess.isdigit():
            self.show_error("Please enter a valid number between 1-100")
            return

        guess_num = int(guess)
        if not 1 <= guess_num <= 100:
            self.show_error("Number must be between 1 and 100!")
            return

        self.attempts += 1
        self.progress["value"] = self.attempts
        self.guess_history.append(guess_num)

        if guess_num == self.secret_number:
            self.game_won()
        else:
            self.process_incorrect_guess(guess_num)

        self.guess_entry.delete(0, tk.END)
        self.update_history()

        if self.attempts >= self.max_attempts:
            self.game_lost()

        if self.attempts % 3 == 0:
            self.give_hint()

    def process_incorrect_guess(self, guess):
        self.current_score = max(0, self.current_score - 50)
        self.update_score()

        direction = "HIGH" if guess > self.secret_number else "LOW"
        color = self.colors["warning"] if direction == "HIGH" else self.colors["highlight"]
        self.status_label.config(
            text=f"Too {direction}! Attempt {self.attempts}/{self.max_attempts}",
            foreground=color
        )
        winsound.Beep(1000 if direction == "HIGH" else 500, 200)

    def game_won(self):
        self.game_active = False
        winsound.Beep(2000, 500)
        messagebox.showinfo(
            "Victory! 🎉",
            f"Congratulations!\nYou found the number in {self.attempts} attempts!\n"
            f"Final Score: {self.current_score}"
        )
        self.disable_game()

    def game_lost(self):
        self.game_active = False
        self.status_label.config(
            text=f"Game Over! The number was {self.secret_number}",
            foreground=self.colors["warning"]
        )
        winsound.Beep(200, 1000)
        messagebox.showinfo(
            "Game Over 💀",
            f"Better luck next time!\nThe secret number was {self.secret_number}"
        )
        self.disable_game()

    def give_hint(self):
        hints = [
            lambda: f"Number is {'even' if self.secret_number % 2 == 0 else 'odd'}",
            lambda: f"Digit sum: {sum(map(int, str(self.secret_number)))}",
            lambda: f"Range: {self.secret_number // 10 * 10}-{self.secret_number // 10 * 10 + 10}",
            lambda: f"Divisible by: {random.choice([n for n in range(2, 10) if self.secret_number % n == 0])}"
            if any(self.secret_number % n == 0 for n in range(2, 10)) else "Prime number!"
        ]

        hint = random.choice(hints)()
        self.hint_count += 1
        self.hint_label.config(text=f"💡 Hint ({self.hint_count}): {hint}")
        winsound.Beep(1500, 300)

    def update_display(self, message):
        self.status_label.config(text=message)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.current_score}")

    def update_history(self):
        self.history_display.config(state="normal")
        last_guess = self.guess_history[-1]
        direction = "⬇️" if last_guess < self.secret_number else "⬆️"
        self.history_display.insert(tk.END, f"Attempt {self.attempts}: {last_guess} {direction}\n")
        self.history_display.see(tk.END)
        self.history_display.config(state="disabled")

    def clear_history(self):
        self.history_display.config(state="normal")
        self.history_display.delete(1.0, tk.END)
        self.history_display.config(state="disabled")

    def disable_game(self):
        self.game_active = False
        self.guess_entry.config(state="disabled")
        self.submit_btn.config(state="disabled")
        self.reset_btn.config(state="normal")

    def reset_game(self):
        if messagebox.askyesno("Confirm Reset", "Start a new game?"):
            self.set_level(self.max_attempts)

    def show_error(self, message):
        winsound.Beep(300, 500)
        messagebox.showerror("Input Error", message)

    def show_help(self):
        help_text = (
            "How to Play:\n\n"
            "1. Choose a difficulty level\n"
            "2. Guess numbers between 1-100\n"
            "3. Get hints every 3 attempts\n"
            "4. Earn maximum score by guessing quickly\n\n"
            "Features:\n"
            "- Score decreases with each attempt\n"
            "- Progress bar shows attempts used\n"
            "- History tracks previous guesses\n"
            "- Multiple hint types available"
        )
        messagebox.showinfo("Game Help", help_text)


if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()