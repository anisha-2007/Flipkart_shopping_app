import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Open another Python page
def open_page(page):
    pages = {
        "browse": "browseproduct.py",
        "orders": "orders_tracking.py"
    }

    if page in pages:
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            pages[page]
        )

        if os.path.isfile(file_path):
            try:
                subprocess.Popen([sys.executable, file_path])
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Could not open page:\n{e}"
                )
        else:
            messagebox.showerror(
                "File Not Found",
                f"{pages[page]} was not found."
            )
    else:
        messagebox.showinfo(
            "Connection Pending",
            f"{page} page connection pending."
        )


# Login function
def login():
    email = email_entry.get().strip()
    password = password_entry.get()

    if email and password:
        messagebox.showinfo(
            "Login Success",
            "Login successful!"
        )

        root.withdraw()

        dashboard = tk.Toplevel(root)
        dashboard.title("Flipkart Customer Dashboard")
        dashboard.geometry("450x450")
        dashboard.configure(bg="white")

        def close_dashboard():
            dashboard.destroy()
            root.deiconify()

        dashboard.protocol("WM_DELETE_WINDOW", close_dashboard)

        tk.Label(
            dashboard,
            text="Welcome to Flipkart",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="blue"
        ).pack(pady=20)

        tk.Button(
            dashboard,
            text="Browse Products",
            width=25,
            height=2,
            command=lambda: open_page("browse")
        ).pack(pady=10)

        tk.Button(
            dashboard,
            text="My Wishlist",
            width=25,
            height=2,
            command=lambda: open_page("wishlist")
        ).pack(pady=10)

        tk.Button(
            dashboard,
            text="My Orders",
            width=25,
            height=2,
            command=lambda: open_page("orders")
        ).pack(pady=10)

        tk.Button(
            dashboard,
            text="Account Details",
            width=25,
            height=2,
            command=lambda: open_page("account")
        ).pack(pady=10)

    else:
        messagebox.showerror(
            "Error",
            "Please enter Email and Password."
        )


# Main login window
root = tk.Tk()
root.title("Flipkart Customer Login")
root.geometry("450x400")
root.configure(bg="white")

tk.Label(
    root,
    text="Flipkart Customer Login",
    font=("Arial", 18, "bold"),
    bg="white",
    fg="blue"
).pack(pady=20)

tk.Label(
    root,
    text="Email / Phone Number",
    bg="white"
).pack()

email_entry = tk.Entry(root, width=35)
email_entry.pack(pady=5)

tk.Label(
    root,
    text="Password",
    bg="white"
).pack()

password_entry = tk.Entry(root, show="*", width=35)
password_entry.pack(pady=5)

tk.Button(
    root,
    text="Login",
    command=login,
    bg="blue",
    fg="white",
    width=18
).pack(pady=20)

root.mainloop()
