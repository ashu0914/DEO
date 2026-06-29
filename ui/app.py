import customtkinter as ctk

ctk.set_appearance_mode("dark")

class DeoUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DEO SYSTEM INTERFACE")
        self.geometry("400x550")
        self.configure(fg_color="#0A0A0A") # Ultra deep black
        self.attributes("-topmost", True)  # Keeps widget pinned on top
        
        # Header title panel
        self.title_label = ctk.CTkLabel(
            self, text="DEO : ONLINE", 
            font=ctk.CTkFont(family="Courier", size=22, weight="bold"),
            text_color="#FF1A1A" # Venom crimson accent
        )
        self.title_label.pack(pady=25)
        
        # Terminal visualizer window
        self.console_box = ctk.CTkTextbox(
            self, width=340, height=350, 
            fg_color="#121212", border_color="#FF1A1A", border_width=1,
            text_color="#FFFFFF", font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.console_box.pack(pady=10)
        self.console_box.insert("0.0", ">> Systems fully initialized...\n>> Awaiting voice inputs, Ashu...\n")
        
    def log_message(self, text):
        self.console_box.insert("end", f"\n>> {text}")
        self.console_box.see("end")

if __name__ == "__main__":
    app = DeoUI()
    app.mainloop()
    