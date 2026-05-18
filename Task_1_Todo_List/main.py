import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import json
import os

# Set the visual theme of our application
ctk.set_appearance_mode("Dark")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure Window settings
        self.title("Premium Task Manager")
        self.geometry("450x550")
        self.resizable(False, False)

        # Data file path for persistent storage
        self.file_path = "tasks.json"
        self.tasks = self.load_tasks()

        # --- UI LAYOUT DESIGN ---
        
        # Title Banner
        self.title_label = ctk.CTkLabel(self, text="MY TO-DO LIST", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # Input Frame (Holds entry field and add button side-by-side)
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter a new task here...", height=40)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Bind the Enter key to automatically add a task
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.add_button = ctk.CTkButton(self.input_frame, text="+ Add", width=90, height=40, font=ctk.CTkFont(weight="bold"), command=self.add_task)
        self.add_button.pack(side="right")

        # Scrollable Frame to display tasks cleanly
        self.tasks_frame = ctk.CTkScrollableFrame(self, label_text="Active Tasks", label_font=ctk.CTkFont(size=14, weight="bold"))
        self.tasks_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Action Buttons Frame at the bottom
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(pady=(10, 20), padx=20, fill="x")

        self.delete_button = ctk.CTkButton(self.action_frame, text="Delete Selected", fg_color="#C0392B", hover_color="#A93226", font=ctk.CTkFont(weight="bold"), command=self.delete_task)
        self.delete_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.clear_button = ctk.CTkButton(self.action_frame, text="Clear All", fg_color="#7F8C8D", hover_color="#95A5A6", font=ctk.CTkFont(weight="bold"), command=self.clear_all_tasks)
        self.clear_button.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # Render existing tasks onto screen on startup
        self.render_tasks()

    # --- CORE APPLICATION LOGIC ---

    def load_tasks(self):
        """Loads tasks safely from JSON file; handles file creation if missing."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return [] # Return empty list if file is corrupted
        return []

    def save_tasks_to_file(self):
        """Persists the current state of tasks to the local storage."""
        with open(self.file_path, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def render_tasks(self):
        """Refreshes and draws the checkbox list inside the UI scroll view."""
        # Clear existing widgets inside scroll frame to avoid duplicates
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        self.checkboxes = []
        for index, task in enumerate(self.tasks):
            # Track state using a BooleanVar
            var = tk.BooleanVar(value=task["completed"])
            
            # Create interactive modern checkbox
            cb = ctk.CTkCheckBox(
                self.tasks_frame, 
                text=task["text"], 
                variable=var,
                font=ctk.CTkFont(size=13),
                command=lambda i=index, v=var: self.toggle_task(i, v)
            )
            cb.pack(anchor="w", pady=8, padx=10)
            
            # Change text styling slightly if already marked completed
            if task["completed"]:
                cb.configure(text_color="gray")
                
            self.checkboxes.append((cb, var))

    def add_task(self):
        """Validates entry fields and safely introduces a new task item."""
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Empty Input", "You cannot add an empty task!")
            return

        self.tasks.append({"text": task_text, "completed": False})
        self.save_tasks_to_file()
        self.render_tasks()
        self.task_entry.delete(0, "end") # Clear text entry field

    def toggle_task(self, index, variable):
        """Updates completion states when checkboxes are clicked."""
        self.tasks[index]["completed"] = variable.get()
        self.save_tasks_to_file()
        self.render_tasks()

    def delete_task(self):
        """Removes marked tasks based on UI selection."""
        # Loop backwards to prevent indexing issues when shifting list size
        updated_tasks = []
        for index, (cb, var) in enumerate(self.checkboxes):
            if not var.get():
                updated_tasks.append(self.tasks[index])
        
        if len(updated_tasks) == len(self.tasks):
            messagebox.showinfo("Selection Missing", "Please check/select the tasks you wish to delete first.")
            return

        self.tasks = updated_tasks
        self.save_tasks_to_file()
        self.render_tasks()

    def clear_all_tasks(self):
        """Wipes the data clean after an explicit user confirmation."""
        if not self.tasks:
            return
        if messagebox.askyesno("Confirm Action", "Are you absolutely sure you want to clear all tasks?"):
            self.tasks = []
            self.save_tasks_to_file()
            self.render_tasks()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
