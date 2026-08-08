import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CampusHub")
app.geometry("900x600")

title = ctk.CTkLabel(
    app,
    text="CampusHub",
    font=("Arial", 32, "bold")
)
title.pack(pady=(80, 10))

subtitle = ctk.CTkLabel(
    app,
    text="Student Management System",
    font=("Arial", 18)
)
subtitle.pack(pady=5)

start_button = ctk.CTkButton(
    app,
    text="Get Started",
    width=200,
    height=45
)
start_button.pack(pady=40)

app.mainloop()