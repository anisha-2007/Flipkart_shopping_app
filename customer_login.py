import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import uuid
from datetime import datetime

DATA_FILE = "flipkart_data.json"

PRODUCTS = [
    {"id": "P101", "name": "Samsung Galaxy Phone", "price": 15999, "category": "Mobiles"},
    {"id": "P102", "name": "iPhone", "price": 59999, "category": "Mobiles"},
    {"id": "P103", "name": "HP Laptop", "price": 45999, "category": "Electronics"},
    {"id": "P104", "name": "Boat Headphones", "price": 1499, "category": "Electronics"},
    {"id": "P105", "name": "Smart Watch", "price": 2499, "category": "Electronics"},
    {"id": "P106", "name": "Men T-Shirt", "price": 599, "category": "Fashion"},
    {"id": "P107", "name": "Women Handbag", "price": 1299, "category": "Fashion"},
    {"id": "P108", "name": "Running Shoes", "price": 1999, "category": "Fashion"},
    {"id": "P109", "name": "Bluetooth Speaker", "price": 1799, "category": "Electronics"},
    {"id": "P110", "name": "Tablet", "price": 12999, "category": "Electronics"},
]


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            pass
    return {"users": {}, "orders": []}


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


data = load_data()


class FlipkartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flipkart Shopping App")
        self.root.geometry("900x620")
        self.root.minsize(760, 520)

        self.phone = ""
        self.user = {}
        self.cart = {}
        self.wishlist = []

        self.blue = "#2874F0"
        self.root.configure(bg="white")
        self.login_page()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def heading(self, parent, text):
        tk.Label(
            parent, text=text, font=("Arial", 21, "bold"),
            fg=self.blue, bg="white"
        ).pack(pady=12)

    def button(self, parent, text, command):
        return tk.Button(
            parent, text=text, command=command,
            bg=self.blue, fg="white", activebackground="#1558c0",
            activeforeground="white", font=("Arial", 10, "bold"),
            padx=10, pady=7, cursor="hand2"
        )

    # LOGIN / REGISTRATION
    def login_page(self):
        self.clear()
        frame = tk.Frame(self.root, bg="white")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        self.heading(frame, "Welcome to Flipkart")
        tk.Label(
            frame, text="Login with your phone number",
            bg="white", font=("Arial", 12)
        ).pack(pady=8)

        tk.Label(frame, text="Phone Number", bg="white").pack(anchor="w")
        self.phone_entry = tk.Entry(frame, width=32, font=("Arial", 12))
        self.phone_entry.pack(pady=6)

        tk.Label(frame, text="Password", bg="white").pack(anchor="w")
        self.password_entry = tk.Entry(
            frame, width=32, show="*", font=("Arial", 12)
        )
        self.password_entry.pack(pady=6)

        self.button(frame, "Login / Register", self.login).pack(
            fill="x", pady=12
        )
        tk.Label(
            frame,
            text="First login: enter your phone number and create a password.",
            bg="white", fg="gray", wraplength=340
        ).pack()

        self.phone_entry.focus_set()
        self.root.bind("<Return>", lambda event: self.login())

    def login(self):
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get()

        if not phone or not password:
            messagebox.showerror("Error", "Enter phone number and password.")
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror(
                "Invalid Phone", "Enter a valid 10-digit phone number."
            )
            return

        if len(password) < 4:
            messagebox.showerror(
                "Invalid Password", "Password must have at least 4 characters."
            )
            return

        key = phone
        if key not in data["users"]:
            data["users"][key] = {
                "phone": phone,
                "password": password,
                "name": "Customer",
                "email": "",
                "address": "",
            }
            save_data()
            messagebox.showinfo(
                "Registered", "Account created successfully!"
            )
        elif data["users"][key]["password"] != password:
            messagebox.showerror(
                "Login Failed", "Incorrect phone number or password."
            )
            return

        self.phone = phone
        self.user = data["users"][key]
        self.cart = {}
        self.wishlist = self.user.setdefault("wishlist", [])
        self.root.unbind("<Return>")
        self.dashboard()

    # DASHBOARD
    def dashboard(self):
        self.clear()
        self.heading(self.root, "Flipkart Shopping Dashboard")

        tk.Label(
            self.root, text=f"Welcome, {self.user.get('name', 'Customer')}!",
            bg="white", font=("Arial", 13)
        ).pack(pady=5)

        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=15)

        actions = [
            ("Browse Products", self.products_page),
            ("My Cart", self.cart_page),
            ("Wishlist", self.wishlist_page),
            ("Place / Track Orders", self.orders_page),
            ("Account Details", self.account_page),
        ]

        for label, command in actions:
            self.button(frame, label, command).pack(
                fill="x", pady=7, ipadx=25
            )

        tk.Label(
            self.root,
            text="Select a section to continue shopping.",
            bg="white", fg="gray"
        ).pack(pady=10)

        self.button(self.root, "Logout", self.logout).pack(pady=8)

    def logout(self):
        self.phone = ""
        self.user = {}
        self.cart = {}
        self.wishlist = []
        self.login_page()

    def page_header(self, title):
        self.clear()
        top = tk.Frame(self.root, bg="white")
        top.pack(fill="x", padx=15, pady=8)

        self.button(top, "← Dashboard", self.dashboard).pack(side="left")
        tk.Label(
            top, text=title, bg="white", fg=self.blue,
            font=("Arial", 18, "bold")
        ).pack(side="left", padx=25)

    # BROWSE PRODUCTS
    def products_page(self):
        self.page_header("Browse Products")

        search_frame = tk.Frame(self.root, bg="white")
        search_frame.pack(fill="x", padx=18, pady=8)

        tk.Label(
            search_frame, text="Search:", bg="white"
        ).pack(side="left")

        search = tk.Entry(search_frame, width=30)
        search.pack(side="left", padx=8)

        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=18, pady=5)

        columns = ("id", "name", "category", "price")
        tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=13
        )
        tree.heading("id", text="Product ID")
        tree.heading("name", text="Product Name")
        tree.heading("category", text="Category")
        tree.heading("price", text="Price (₹)")

        tree.column("id", width=100)
        tree.column("name", width=280)
        tree.column("category", width=150)
        tree.column("price", width=120, anchor="e")

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def refresh(*args):
            query = search.get().lower().strip()
            tree.delete(*tree.get_children())
            for p in PRODUCTS:
                if (query in p["name"].lower()
                        or query in p["category"].lower()
                        or query in p["id"].lower()):
                    tree.insert(
                        "", "end",
                        values=(p["id"], p["name"], p["category"],
                                f"{p['price']:,}")
                    )

        search.bind("<KeyRelease>", refresh)
        refresh()

        def selected_product():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning(
                    "Select Product", "Please select a product first."
                )
                return None
            product_id = tree.item(selection[0], "values")[0]
            return next(p for p in PRODUCTS if p["id"] == product_id)

        controls = tk.Frame(self.root, bg="white")
        controls.pack(pady=10)

        def add_cart():
            p = selected_product()
            if p:
                self.cart[p["id"]] = self.cart.get(p["id"], 0) + 1
                messagebox.showinfo(
                    "Added", f"{p['name']} added to your cart."
                )

        def add_wishlist():
            p = selected_product()
            if p:
                if p["id"] not in self.wishlist:
                    self.wishlist.append(p["id"])
                    self.user["wishlist"] = self.wishlist
                    save_data()
                messagebox.showinfo(
                    "Wishlist", f"{p['name']} added to wishlist."
                )

        self.button(controls, "Add to Cart", add_cart).pack(
            side="left", padx=6
        )
        self.button(controls, "Add to Wishlist", add_wishlist).pack(
            side="left", padx=6
        )
        self.button(
            controls, "Open Cart", self.cart_page
        ).pack(side="left", padx=6)

    # CART AND CHECKOUT
    def cart_page(self):
        self.page_header("My Cart")
        body = tk.Frame(self.root, bg="white")
        body.pack(fill="both", expand=True, padx=25, pady=15)

        if not self.cart:
            tk.Label(
                body, text="Your cart is empty.",
                bg="white", font=("Arial", 13)
            ).pack(pady=30)
            return

        total = 0
        for product_id, quantity in self.cart.items():
            p = next(p for p in PRODUCTS if p["id"] == product_id)
            amount = p["price"] * quantity
            total += amount
            tk.Label(
                body,
                text=f"{p['name']}  |  ₹{p['price']:,} × {quantity}"
                     f"  =  ₹{amount:,}",
                bg="white", font=("Arial", 12)
            ).pack(anchor="w", pady=5)

        tk.Label(
            body, text=f"Total: ₹{total:,}",
            bg="white", font=("Arial", 16, "bold"), fg=self.blue
        ).pack(pady=15)

        def checkout():
            if not self.cart:
                return

            order_id = "FK" + uuid.uuid4().hex[:8].upper()
            items = []
            grand_total = 0

            for product_id, quantity in self.cart.items():
                p = next(p for p in PRODUCTS if p["id"] == product_id)
                items.append({
                    "id": p["id"],
                    "name": p["name"],
                    "price": p["price"],
                    "quantity": quantity,
                })
                grand_total += p["price"] * quantity

            order = {
                "order_id": order_id,
                "phone": self.phone,
                "items": items,
                "total": grand_total,
                "status": "Order Placed",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            data["orders"].append(order)
            save_data()
            self.cart.clear()

            messagebox.showinfo(
                "Order Successful",
                f"Your order has been placed!\n\nOrder ID: {order_id}"
                f"\nTotal: ₹{grand_total:,}\n\nSave your Order ID to track it."
            )
            self.orders_page()

        self.button(body, "Place Order", checkout).pack(pady=10)

    # WISHLIST
    def wishlist_page(self):
        self.page_header("My Wishlist")
        body = tk.Frame(self.root, bg="white")
        body.pack(fill="both", expand=True, padx=25, pady=15)

        if not self.wishlist:
            tk.Label(
                body, text="Your wishlist is empty.",
                bg="white", font=("Arial", 13)
            ).pack(pady=25)
            return

        for product_id in self.wishlist[:]:
            p = next((p for p in PRODUCTS if p["id"] == product_id), None)
            if not p:
                continue

            row = tk.Frame(body, bg="white")
            row.pack(fill="x", pady=5)
            tk.Label(
                row, text=f"{p['name']} — ₹{p['price']:,}",
                bg="white", font=("Arial", 11)
            ).pack(side="left")

            def add_to_cart(pid=product_id):
                self.cart[pid] = self.cart.get(pid, 0) + 1
                messagebox.showinfo("Cart", "Product added to cart.")

            def remove(pid=product_id):
                if pid in self.wishlist:
                    self.wishlist.remove(pid)
                self.user["wishlist"] = self.wishlist
                save_data()
                self.wishlist_page()

            self.button(row, "Add to Cart", add_to_cart).pack(
                side="right", padx=4
            )
            self.button(row, "Remove", remove).pack(side="right", padx=4)

    # MY ORDERS AND ORDER TRACKING
    def orders_page(self):
        self.page_header("My Orders & Tracking")

        my_orders = [
            order for order in data["orders"]
            if order["phone"] == self.phone
        ]

        tk.Label(
            self.root, text="Your Orders",
            bg="white", font=("Arial", 13, "bold")
        ).pack(pady=5)

        order_frame = tk.Frame(self.root, bg="white")
        order_frame.pack(fill="both", expand=True, padx=20)

        if not my_orders:
            tk.Label(
                order_frame, text="No orders yet. Browse products to order.",
                bg="white"
            ).pack(pady=15)
        else:
            tree = ttk.Treeview(
                order_frame,
                columns=("id", "date", "total", "status"),
                show="headings", height=7
            )
            for col, title in [
                ("id", "Order ID"), ("date", "Date"),
                ("total", "Total (₹)"), ("status", "Status")
            ]:
                tree.heading(col, text=title)

            for order in my_orders:
                tree.insert(
                    "", "end",
                    values=(
                        order["order_id"], order["date"],
                        f"{order['total']:,}", order["status"]
                    )
                )
            tree.pack(fill="both", expand=True)

        track_frame = tk.Frame(self.root, bg="white")
        track_frame.pack(fill="x", padx=20, pady=15)

        tk.Label(
            track_frame, text="Enter Order ID to track:",
            bg="white"
        ).pack(side="left")

        order_entry = tk.Entry(track_frame, width=25)
        order_entry.pack(side="left", padx=8)

        result = tk.Label(
            self.root, text="", bg="white",
            font=("Arial", 11), justify="left"
        )
        result.pack(pady=8)

        def track_order():
            oid = order_entry.get().strip().upper()
            order = next(
                (o for o in data["orders"]
                 if o["order_id"] == oid and o["phone"] == self.phone),
                None
            )

            if not order:
                result.config(
                    text="Order not found. Check your Order ID.",
                    fg="red"
                )
                return

            item_text = "\n".join(
                f"• {item['name']} × {item['quantity']}"
                for item in order["items"]
            )
            result.config(
                text=f"Order ID: {order['order_id']}\n"
                     f"Items:\n{item_text}\n"
                     f"Total: ₹{order['total']:,}\n"
                     f"Status: {order['status']}\n"
                     f"Order Date: {order['date']}",
                fg="green"
            )

        self.button(track_frame, "Track Order", track_order).pack(
            side="left"
        )

    # ACCOUNT DETAILS
    def account_page(self):
        self.page_header("Account Details")
        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=20)

        tk.Label(
            frame, text="Update Your Profile",
            bg="white", font=("Arial", 15, "bold")
        ).pack(pady=10)

        fields = {}
        details = [
            ("Name", "name"),
            ("Phone Number", "phone"),
            ("Email", "email"),
            ("Address", "address"),
        ]

        for label, key in details:
            row = tk.Frame(frame, bg="white")
            row.pack(fill="x", pady=7)
            tk.Label(
                row, text=label, width=16, anchor="w", bg="white"
            ).pack(side="left")
            entry = tk.Entry(row, width=38)
            entry.pack(side="left")
            entry.insert(0, self.user.get(key, ""))
            fields[key] = entry

            if key == "phone":
                entry.config(state="readonly")

        def save_profile():
            name = fields["name"].get().strip()
            email = fields["email"].get().strip()
            address = fields["address"].get().strip()

            if not name:
                messagebox.showerror("Error", "Name cannot be empty.")
                return

            self.user["name"] = name
            self.user["email"] = email
            self.user["address"] = address
            data["users"][self.phone] = self.user
            save_data()
            messagebox.showinfo(
                "Saved", "Account details updated successfully."
            )

        self.button(frame, "Save Account Details", save_profile).pack(
            pady=15
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = FlipkartApp(root)
    root.mainloop()
