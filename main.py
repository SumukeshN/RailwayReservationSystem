import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import json
import os

# File paths
USER_FILE = "users.json"
BOOKING_FILE = "bookings.json"

# Load Data
def load_data():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            users.update(json.load(f))
    if os.path.exists(BOOKING_FILE):
        with open(BOOKING_FILE, "r") as f:
            bookings.update(json.load(f))

# Save Data
def save_data():
    with open(USER_FILE, "w") as f:
        json.dump(users, f)
    with open(BOOKING_FILE, "w") as f:
        json.dump(bookings, f)

# Initialize data
users = {}
bookings = {}
load_data()

# Train List
trains = [
    "🚄 Rajdhani Express", "🚆 Shatabdi Express", "🚅 Duronto Express",
    "🚈 Vande Bharat", "🚋 Humsafar Express", "🚃 Garib Rath"
]

# UI Styles
COLORS = {
    "bg": "#f0f8ff",
    "card": "#ffffff",
    "button": "#1976d2",
    "button_hover": "#0d47a1",
    "text": "#0d47a1"
}
FONTS = {
    "header": ("Segoe UI Semibold", 22),
    "text": ("Segoe UI", 12),
    "button": ("Segoe UI", 11)
}

# Background image utility
def set_background(window, path):
    try:
        img = Image.open(path).resize((800, 600))
        bg = ImageTk.PhotoImage(img)
        label = tk.Label(window, image=bg)
        label.image = bg
        label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        window.configure(bg=COLORS["bg"])

# Styled button utility
def styled_button(parent, text, command):
    return tk.Button(parent, text=text, command=command,
                     font=FONTS["button"], bg=COLORS["button"],
                     fg="white", activebackground=COLORS["button_hover"],
                     relief="flat", cursor="hand2", padx=10, pady=6)

# Register Window
def register_screen():
    win = tk.Tk()
    win.title("Register - Railway Booking")
    win.geometry("400x400")
    win.resizable(False, False)
    set_background(win, "train_bg.png")

    frame = tk.Frame(win, bg=COLORS["card"], padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="📝 Register", font=FONTS["header"], fg=COLORS["text"], bg=COLORS["card"]).pack(pady=10)

    tk.Label(frame, text="Username", font=FONTS["text"], bg=COLORS["card"]).pack()
    username = tk.Entry(frame, font=FONTS["text"])
    username.pack(pady=5)

    tk.Label(frame, text="Password", font=FONTS["text"], bg=COLORS["card"]).pack()
    password = tk.Entry(frame, font=FONTS["text"], show="*")
    password.pack(pady=5)

    def register():
        u, p = username.get(), password.get()
        if not u or not p:
            messagebox.showwarning("Input Error", "All fields are required.")
        elif u in users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            users[u] = p
            save_data()
            messagebox.showinfo("Success", "Registration successful!")
            win.destroy()
            login_screen()

    styled_button(frame, "Register", register).pack(pady=15)
    tk.Button(frame, text="← Back to Login", font=FONTS["text"], bg=COLORS["card"],
              fg=COLORS["text"], relief="flat", command=lambda: [win.destroy(), login_screen()]).pack()
    win.mainloop()

# Login Window
def login_screen():
    win = tk.Tk()
    win.title("Login - Railway Booking")
    win.geometry("400x400")
    win.resizable(False, False)
    set_background(win, "train_bg.png")

    frame = tk.Frame(win, bg=COLORS["card"], padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="🚆 Login", font=FONTS["header"], fg=COLORS["text"], bg=COLORS["card"]).pack(pady=10)

    tk.Label(frame, text="Username", font=FONTS["text"], bg=COLORS["card"]).pack()
    username = tk.Entry(frame, font=FONTS["text"])
    username.pack(pady=5)

    tk.Label(frame, text="Password", font=FONTS["text"], bg=COLORS["card"]).pack()
    password = tk.Entry(frame, font=FONTS["text"], show="*")
    password.pack(pady=5)

    def login():
        u, p = username.get(), password.get()
        if users.get(u) == p:
            messagebox.showinfo("Welcome", f"Hello {u}!")
            win.destroy()
            dashboard(u)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    styled_button(frame, "Login", login).pack(pady=15)
    tk.Button(frame, text="New User? Register →", font=FONTS["text"], bg=COLORS["card"],
              fg=COLORS["text"], relief="flat", command=lambda: [win.destroy(), register_screen()]).pack()
    win.mainloop()

# Dashboard
def dashboard(username):
    win = tk.Tk()
    win.title("Dashboard - Railway Booking")
    win.geometry("800x600")
    win.resizable(True, True)
    set_background(win, "train_bg.png")

    tk.Label(win, text=f"Welcome, {username} 🚉", font=FONTS["header"],
             bg=COLORS["text"], fg="white", pady=10).pack(fill="x")

    selected = tk.StringVar(value="")

    list_frame = tk.Frame(win, bg=COLORS["card"], padx=20, pady=10)
    list_frame.pack(pady=20)

    tk.Label(list_frame, text="Select a Train:", font=FONTS["text"],
             bg=COLORS["card"], fg=COLORS["text"]).pack(pady=5)

    for train in trains:
        tk.Radiobutton(list_frame, text=train, variable=selected, value=train,
                       font=FONTS["text"], bg=COLORS["card"], anchor="w",
                       selectcolor="#cce7ff", width=40, indicatoron=False).pack(pady=3)

    def book_ticket():
        sel = selected.get()
        if not sel:
            messagebox.showwarning("Select Train", "Please choose a train.")
        else:
            bookings.setdefault(username, []).append(sel)
            save_data()
            messagebox.showinfo("Booked", f"Ticket booked for: {sel}")

    def view_bookings():
        hist = bookings.get(username, [])
        messagebox.showinfo("Your Tickets", "\n".join(hist) if hist else "No bookings yet.")

    def cancel_ticket():
        hist = bookings.get(username, [])
        if not hist:
            messagebox.showinfo("No Bookings", "No tickets to cancel.")
            return

        def do_cancel():
            item = combo.get()
            if item in bookings[username]:
                bookings[username].remove(item)
                save_data()
                messagebox.showinfo("Cancelled", f"Cancelled ticket: {item}")
                top.destroy()

        top = tk.Toplevel(win)
        top.title("Cancel Ticket")
        top.geometry("300x200")
        tk.Label(top, text="Select Ticket to Cancel:", font=FONTS["text"]).pack(pady=10)
        combo = ttk.Combobox(top, values=hist, state="readonly", font=FONTS["text"])
        combo.pack(pady=5)
        styled_button(top, "Cancel", do_cancel).pack(pady=10)

    btn_frame = tk.Frame(win, bg=COLORS["card"], padx=20, pady=20)
    btn_frame.pack(pady=10)

    styled_button(btn_frame, "🎟️ Book Ticket", book_ticket).pack(pady=5, fill="x")
    styled_button(btn_frame, "📋 View Bookings", view_bookings).pack(pady=5, fill="x")
    styled_button(btn_frame, "❌ Cancel Ticket", cancel_ticket).pack(pady=5, fill="x")
    styled_button(btn_frame, "🔓 Logout", lambda: [win.destroy(), login_screen()]).pack(pady=10, fill="x")

    win.mainloop()

# Launch the app
if __name__ == "__main__":
    login_screen()
