import tkinter as tk
from tkinter import messagebox
import requests
import hashlib

class PasswordStrengthChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.dark_mode = False  # Default mode is Bright Mode
        
        self.root.configure(bg="white")
        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(padx=20, pady=20)
        
        self.label = tk.Label(self.frame, text="Enter your password:", bg="white", font=("Arial", 12))
        self.label.grid(row=0, column=0, columnspan=2, pady=5)
        
        self.password_entry = tk.Entry(self.frame, show="*", width=30, font=("Arial", 12))
        self.password_entry.grid(row=1, column=0, columnspan=2, pady=5)
        self.password_entry.bind("<KeyRelease>", self.check_strength)
        
        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbox = tk.Checkbutton(self.frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password, bg="white")
        self.show_password_checkbox.grid(row=2, column=0, columnspan=2, pady=5)
        
        self.criteria_labels = {}
        self.criteria = {
            "At least 8 characters": lambda pwd: len(pwd) >= 8,
            "At least 1 uppercase letter": lambda pwd: any(c.isupper() for c in pwd),
            "At least 1 lowercase letter": lambda pwd: any(c.islower() for c in pwd),
            "At least 1 digit": lambda pwd: any(c.isdigit() for c in pwd),
            "At least 1 special character": lambda pwd: any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in pwd),
        }
        
        self.criteria_frame = tk.Frame(self.frame, bg="white")
        self.criteria_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        for idx, (text, _) in enumerate(self.criteria.items()):
            self.criteria_labels[text] = tk.Label(self.criteria_frame, text=f"{text}: ❌", bg="white", font=("Arial", 10))
            self.criteria_labels[text].grid(row=idx, column=0, sticky="w")
        
        self.strength_label = tk.Label(self.frame, text="Strength: N/A", bg="white", font=("Arial", 12, "bold"))
        self.strength_label.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.hibp_button = tk.Button(self.frame, text="Have I Been Pwned", command=self.check_hibp)
        self.hibp_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        self.hibp_result_label = tk.Label(self.frame, text="HIBP Result: N/A", bg="white", font=("Arial", 12))
        self.hibp_result_label.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset_fields)
        self.reset_button.grid(row=7, column=0, columnspan=2, pady=5)
        
        self.theme_button = tk.Button(self.frame, text="Switch to Dark Mode", command=self.toggle_theme)
        self.theme_button.grid(row=8, column=0, columnspan=2, pady=5)
    
    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def check_strength(self, event=None):
        password = self.password_entry.get()
        passed_criteria = sum(check(password) for check in self.criteria.values())
        
        for text, check in self.criteria.items():
            self.criteria_labels[text].config(text=f"{text}: {'✔️' if check(password) else '❌'}")
        
        if passed_criteria == 5:
            self.strength_label.config(text="Strength: Strong", fg="green")
        elif passed_criteria >= 3:
            self.strength_label.config(text="Strength: Medium", fg="orange")
        else:
            self.strength_label.config(text="Strength: Weak", fg="red")
    
    def check_hibp(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password first.")
            return
        
        sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1_password[:5], sha1_password[5:]
        
        try:
            response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
            if suffix in response.text:
                self.hibp_result_label.config(text="HIBP Result: Compromised", fg="red")
            else:
                self.hibp_result_label.config(text="HIBP Result: Safe", fg="green")
        except Exception:
            messagebox.showerror("Error", "Failed to check password.")
    
    def reset_fields(self):
        self.password_entry.delete(0, tk.END)
        self.hibp_result_label.config(text="HIBP Result: N/A", fg="black")
        self.strength_label.config(text="Strength: N/A", fg="black")
        for text in self.criteria_labels:
            self.criteria_labels[text].config(text=f"{text}: ❌")
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg_color = "#333" if self.dark_mode else "white"
        fg_color = "white" if self.dark_mode else "black"
        btn_text = "Switch to Bright Mode" if self.dark_mode else "Switch to Dark Mode"
        
        self.root.configure(bg=bg_color)
        self.frame.configure(bg=bg_color)
        self.criteria_frame.configure(bg=bg_color)
        
        for widget in self.frame.winfo_children():
            if isinstance(widget, (tk.Label, tk.Checkbutton)):
                widget.config(bg=bg_color, fg=fg_color)
        for widget in self.criteria_frame.winfo_children():
            widget.config(bg=bg_color, fg=fg_color)
        
        self.theme_button.config(text=btn_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()
