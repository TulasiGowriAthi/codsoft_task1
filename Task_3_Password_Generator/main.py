import string
import secrets
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# Set up application window styling
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Secure Password Forge")
        self.geometry("450x500")
        self.resizable(False, False)

        # --- UI ELEMENTS SETUP ---

        # Main App Title Banner
        self.title_label = ctk.CTkLabel(self, text="PASSWORD GENERATOR", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(pady=(20, 15))

        # Output Box Frame (Where the password shows up)
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(pady=10, padx=25, fill="x")

        self.password_display = ctk.CTkEntry(
            self.output_frame, 
            placeholder_text="Your secure password will appear here", 
            height=45, 
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.password_display.pack(pady=15, padx=15, fill="x")

        # Configuration Parameter Frame
        self.config_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.config_frame.pack(pady=10, padx=25, fill="x")

        # Slider for Password Length Selection
        self.length_label = ctk.CTkLabel(self.config_frame, text="Password Length: 12", font=ctk.CTkFont(size=14, weight="bold"))
        self.length_label.pack(anchor="w", pady=(0, 5))

        self.length_slider = ctk.CTkSlider(self.config_frame, from_=8, to=32, number_of_steps=24, command=self.update_slider_label)
        self.length_slider.set(12)  # Set default length slider value to 12
        self.length_slider.pack(fill="x", pady=(0, 15))

        # Complexity Checkbox Variables
        self.use_upper = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        # Interactive Checkbox Widgets
        self.cb_upper = ctk.CTkCheckBox(self.config_frame, text="Include Uppercase Letters (A-Z)", variable=self.use_upper)
        self.cb_upper.pack(anchor="w", pady=6)

        self.cb_digits = ctk.CTkCheckBox(self.config_frame, text="Include Numbers (0-9)", variable=self.use_digits)
        self.cb_digits.pack(anchor="w", pady=6)

        self.cb_symbols = ctk.CTkCheckBox(self.config_frame, text="Include Special Symbols (@, #, $, %)", variable=self.use_symbols)
        self.cb_symbols.pack(anchor="w", pady=6)

        # Bottom Action Control Buttons
        self.generate_btn = ctk.CTkButton(
            self, 
            text="⚡ Generate Password", 
            height=45, 
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.generate_secure_password
        )
        self.generate_btn.pack(pady=(20, 10), padx=25, fill="x")

        self.copy_btn = ctk.CTkButton(
            self, 
            text="📋 Copy to Clipboard", 
            height=40, 
            fg_color="#27AE60", 
            hover_color="#1E8449",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.copy_password_to_clipboard
        )
        self.copy_btn.pack(pady=5, padx=25, fill="x")

    # --- ACTION LOGIC OPERATIONS ---

    def update_slider_label(self, value):
        """Dynamically updates text as user slides the length bar."""
        self.length_label.configure(text=f"Password Length: {int(value)}")

    def generate_secure_password(self):
        """Compiles character pools safely and constructs a random value string."""
        # Lowercase character set remains default foundational anchor
        character_pool = string.ascii_lowercase

        if self.use_upper.get():
            character_pool += string.ascii_uppercase
        if self.use_digits.get():
            character_pool += string.digits
        if self.use_symbols.get():
            character_pool += string.punctuation

        target_length = int(self.length_slider.get())

        # Ensure security check constraints prevent generating from a completely empty selection pool
        if not self.use_upper.get() and not self.use_digits.get() and not self.use_symbols.get() and not character_pool:
            messagebox.showerror("Selection Error", "An unexpected character pool failure occurred.")
            return

        # Secure cryptographic loop execution selection
        generated_password = "".join(secrets.choice(character_pool) for _ in range(target_length))
        
        # Clear output display box and present generated value
        self.password_display.delete(0, "end")
        self.password_display.insert(0, generated_password)

    def copy_password_to_clipboard(self):
        """Intercepts system operational clipboard to hold password string strings."""
        password_string = self.password_display.get()
        
        if not password_string:
            messagebox.showwarning("Clipboard Empty", "Please generate a password first before trying to copy it!")
            return
        
        # Access and pass data value straight to clipboard storage architecture
        self.clipboard_clear()
        self.clipboard_append(password_string)
        messagebox.showinfo("Success", "Password safely copied to system clipboard!")

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
