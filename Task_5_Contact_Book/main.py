import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import json
import os

# Configure application UI styles
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ContactBookApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Executive Contact Directory")
        self.geometry("800x500")
        self.resizable(False, False)

        # File Storage Path
        self.file_path = "contacts.json"
        self.contacts = self.load_contacts()

        # --- UI LAYOUT DESIGN ---
        
        # Left Panel Frame: Input Fields for Adding/Updating
        self.left_panel = ctk.CTkFrame(self, width=320, corner_radius=0)
        self.left_panel.pack(side="left", fill="y", padx=0, pady=0)
        self.left_panel.pack_propagate(False) # Keep width fixed

        self.panel_title = ctk.CTkLabel(self.left_panel, text="CONTACT CARD", font=ctk.CTkFont(size=18, weight="bold"))
        self.panel_title.pack(pady=(20, 20))

        # Entry fields
        self.name_entry = self.create_input_field("Full Name")
        self.phone_entry = self.create_input_field("Phone Number")
        self.email_entry = self.create_input_field("Email Address")
        self.address_entry = self.create_input_field("Physical Address")

        # Action Buttons in Left Panel
        self.add_btn = ctk.CTkButton(self.left_panel, text="➕ Add Contact", font=ctk.CTkFont(weight="bold"), command=self.add_contact)
        self.add_btn.pack(fill="x", padx=20, pady=(15, 10))

        self.update_btn = ctk.CTkButton(self.left_panel, text="🔄 Update Selected", fg_color="#2980B9", hover_color="#2471A3", font=ctk.CTkFont(weight="bold"), command=self.update_contact)
        self.update_btn.pack(fill="x", padx=20, pady=5)

        # Right Panel Frame: Search & Directory List View
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Search Utilities Header
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.render_contacts_list())
        self.search_entry = ctk.CTkEntry(self.right_panel, placeholder_text="🔍 Search contacts by name or phone number...", textvariable=self.search_var, height=35)
        self.search_entry.pack(fill="x", pady=(0, 10))

        # Scrollable area to list all contacts
        self.dir_frame = ctk.CTkScrollableFrame(self.right_panel, label_text="Saved Directory Contacts", label_font=ctk.CTkFont(size=14, weight="bold"))
        self.dir_frame.pack(fill="both", expand=True, pady=5)

        # Bottom Frame for global removal action
        self.bottom_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.bottom_frame.pack(fill="x", pady=(10, 0))

        self.delete_btn = ctk.CTkButton(self.bottom_frame, text="🗑️ Delete Selected Contact", fg_color="#C0392B", hover_color="#A93226", font=ctk.CTkFont(weight="bold"), command=self.delete_contact)
        self.delete_btn.pack(side="right")

        # Initial render on startup
        self.render_contacts_list()

    def create_input_field(self, placeholder):
        """Helper function to create styled text fields easily."""
        entry = ctk.CTkEntry(self.left_panel, placeholder_text=placeholder, height=35)
        entry.pack(fill="x", padx=20, pady=6)
        return entry

    # --- CORE APPLICATION LOGIC ---

    def load_contacts(self):
        """Loads entries from data file safely on startup."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []

    def save_contacts_to_file(self):
        """Writes data down to persistent local storage disk."""
        with open(self.file_path, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def render_contacts_list(self):
        """Dynamically filters and draws rows inside directory view display."""
        for widget in self.dir_frame.winfo_children():
            widget.destroy()

        search_query = self.search_var.get().lower().strip()
        self.radio_var = tk.IntVar(value=-1)

        for index, item in enumerate(self.contacts):
            # Apply instant real-time filtration string checks
            if search_query and (search_query not in item["name"].lower() and search_query not in item["phone"]):
                continue

            # Row wrapper frame
            row = ctk.CTkFrame(self.dir_frame, fg_color="transparent")
            row.pack(fill="x", pady=4, padx=5)

            # Interactive radio selection node matching list index array pointer
            rb = ctk.CTkRadioButton(
                row, 
                text=f"{item['name'].upper()}  |  📱 {item['phone']}", 
                variable=self.radio_var, 
                value=index,
                font=ctk.CTkFont(size=13),
                command=self.load_selected_contact_into_form
            )
            rb.pack(side="left", padx=10, pady=5)

            # Quick detail badge label string display right corner
            badge = ctk.CTkLabel(row, text=f"✉️ {item['email']}", font=ctk.CTkFont(size=11), text_color="gray")
            badge.pack(side="right", padx=15)

    def load_selected_contact_into_form(self):
        """Populates left editing card inputs automatically when selecting an entry row."""
        selected_index = self.radio_var.get()
        if selected_index == -1:
            return
        
        target = self.contacts[selected_index]
        
        # Wipe input forms clean
        self.clear_form_inputs()

        # Re-fill with selected data block text
        self.name_entry.insert(0, target["name"])
        self.phone_entry.insert(0, target["phone"])
        self.email_entry.insert(0, target["email"])
        self.address_entry.insert(0, target["address"])

    def clear_form_inputs(self):
        """Flushes input values clear across fields."""
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.address_entry.delete(0, "end")

    def add_contact(self):
        """Validates card fields and locks down new contact profiles."""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip() or "N/A"
        address = self.address_entry.get().strip() or "N/A"

        if not name or not phone:
            messagebox.showwarning("Fields Missing", "Name and Phone Number are required fields!")
            return

        self.contacts.append({"name": name, "phone": phone, "email": email, "address": address})
        self.save_contacts_to_file()
        self.render_contacts_list()
        self.clear_form_inputs()
        messagebox.showinfo("Success", f"{name} added to directory successfully!")

    def update_contact(self):
        """Overwrites highlighted database nodes with freshly edited field strings."""
        selected_index = self.radio_var.get()
        if selected_index == -1:
            messagebox.showwarning("No Selection", "Please click/select a contact from the list to update first.")
            return

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not name or not phone:
            messagebox.showwarning("Fields Missing", "Name and Phone values cannot be updated to empty strings.")
            return

        self.contacts[selected_index] = {
            "name": name,
            "phone": phone,
            "email": self.email_entry.get().strip() or "N/A",
            "address": self.address_entry.get().strip() or "N/A"
        }
        self.save_contacts_to_file()
        self.render_contacts_list()
        self.clear_form_inputs()
        messagebox.showinfo("Updated", "Contact details successfully overwritten!")

    def delete_contact(self):
        """Removes an active profile cleanly from the application array system."""
        selected_index = self.radio_var.get()
        if selected_index == -1:
            messagebox.showwarning("No Selection", "Please click/select a contact row from the list to remove first.")
            return

        target_name = self.contacts[selected_index]["name"]
        if messagebox.askyesno("Confirm Action", f"Are you sure you want to permanently delete {target_name}?"):
            self.contacts.pop(selected_index)
            self.save_contacts_to_file()
            self.render_contacts_list()
            self.clear_form_inputs()

if __name__ == "__main__":
    app = ContactBookApp()
    app.mainloop()
