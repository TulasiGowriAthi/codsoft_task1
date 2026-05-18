import random
import tkinter as tk
import customtkinter as ctk

# Configure global application visual theme styles
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class RockPaperScissorsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Arena: Rock-Paper-Scissors")
        self.geometry("500x550")
        self.resizable(False, False)

        # Game State Core Variables
        self.user_score = 0
        self.computer_score = 0
        self.choices = ["Rock", "Paper", "Scissors"]

        # --- UI LAYOUT DESIGN ---

        # Main App Header Title Banner
        self.title_label = ctk.CTkLabel(self, text="ROCK, PAPER, SCISSORS", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(pady=(20, 15))

        # Dashboard Frame for Score Tracking display
        self.score_frame = ctk.CTkFrame(self)
        self.score_frame.pack(pady=10, padx=30, fill="x")

        self.player_score_lbl = ctk.CTkLabel(self.score_frame, text="YOU: 0", font=ctk.CTkFont(size=18, weight="bold"), text_color="#3498DB")
        self.player_score_lbl.pack(side="left", padx=35, pady=15)

        self.vs_lbl = ctk.CTkLabel(self.score_frame, text="VS", font=ctk.CTkFont(size=14, weight="bold"), text_color="gray")
        self.vs_lbl.pack(side="left", expand=True)

        self.computer_score_lbl = ctk.CTkLabel(self.score_frame, text="COMP: 0", font=ctk.CTkFont(size=18, weight="bold"), text_color="#E74C3C")
        self.computer_score_lbl.pack(side="right", padx=35, pady=15)

        # Choice Feedback Display Board
        self.display_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.display_frame.pack(pady=15, padx=30, fill="x")

        self.player_choice_lbl = ctk.CTkLabel(self.display_frame, text="Your Choice: —", font=ctk.CTkFont(size=14))
        self.player_choice_lbl.pack(anchor="w", padx=10, pady=2)

        self.comp_choice_lbl = ctk.CTkLabel(self.display_frame, text="Computer's Choice: —", font=ctk.CTkFont(size=14))
        self.comp_choice_lbl.pack(anchor="w", padx=10, pady=2)

        # Status Round Outcome Banner (Dynamic background changes based on outcome)
        self.status_banner = ctk.CTkLabel(
            self, 
            text="Choose your move to begin the battle!", 
            height=50, 
            fg_color="#34495E", 
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_banner.pack(pady=15, padx=30, fill="x")

        # Interactive Choice Control Input Grid Button Frame
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=15, padx=30, fill="x")

        self.rock_btn = ctk.CTkButton(self.btn_frame, text="🪨 Rock", height=45, font=ctk.CTkFont(size=14, weight="bold"), command=lambda: self.play_round("Rock"))
        self.rock_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.paper_btn = ctk.CTkButton(self.btn_frame, text="📄 Paper", height=45, font=ctk.CTkFont(size=14, weight="bold"), command=lambda: self.play_round("Paper"))
        self.paper_btn.pack(side="left", fill="x", expand=True, padx=5)

        self.scissors_btn = ctk.CTkButton(self.btn_frame, text="✂️ Scissors", height=45, font=ctk.CTkFont(size=14, weight="bold"), command=lambda: self.play_round("Scissors"))
        self.scissors_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Core Global State System Reset Operational Button
        self.reset_btn = ctk.CTkButton(
            self, 
            text="🔄 Reset Scoreboard", 
            height=40, 
            fg_color="#7F8C8D", 
            hover_color="#95A5A6",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.reset_scoreboard
        )
        self.reset_btn.pack(pady=(20, 10), padx=30, fill="x")

    # --- CORE GAME MATCH LOGIC ---

    def play_round(self, player_move):
        """Processes user input choice selections against random computer evaluations."""
        computer_move = random.choice(self.choices)

        # Update matching move text labels on screen
        self.player_choice_lbl.configure(text=f"Your Choice: {player_move}")
        self.comp_choice_lbl.configure(text=f"Computer's Choice: {computer_move}")

        # Core matching logic constraints check condition loops
        if player_move == computer_move:
            self.status_banner.configure(text=f"IT'S A TIE! Both chose {player_move.upper()}", fg_color="#7F8C8D")
        
        elif (player_move == "Rock" and computer_move == "Scissors") or \
             (player_move == "Paper" and computer_move == "Rock") or \
             (player_move == "Scissors" and computer_move == "Paper"):
            
            self.user_score += 1
            self.player_score_lbl.configure(text=f"YOU: {self.user_score}")
            self.status_banner.configure(text=f"YOU WIN! {player_move.upper()} beats {computer_move.upper()}", fg_color="#27AE60")
        
        else:
            self.computer_score += 1
            self.computer_score_lbl.configure(text=f"COMP: {self.computer_score}")
            self.status_banner.configure(text=f"YOU LOSE! {computer_move.upper()} beats {player_move.upper()}", fg_color="#C0392B")

    def reset_scoreboard(self):
        """Wipes matching session data scores back cleanly to core defaults."""
        self.user_score = 0
        self.computer_score = 0
        self.player_score_lbl.configure(text="YOU: 0")
        self.computer_score_lbl.configure(text="COMP: 0")
        self.player_choice_lbl.configure(text="Your Choice: —")
        self.comp_choice_lbl.configure(text="Computer's Choice: —")
        self.status_banner.configure(text="Scoreboard reset! Choose your move to begin again.", fg_color="#34495E")

if __name__ == "__main__":
    app = RockPaperScissorsApp()
    app.mainloop()
