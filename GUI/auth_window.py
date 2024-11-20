import tkinter as tk
from tkinter import messagebox
from Authorization.Check_password import Authenticator


class LoginApp:
    def __init__(self, root, authenticator):
        self.root = root
        self.authenticator = authenticator

        # Конфигурация окна
        self.root.title("Login")
        self.root.geometry("300x200")

        # Поля для ввода логина и пароля
        tk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        # Кнопка входа
        tk.Button(root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, role = self.authenticator.verify_user(username, password)
        if success:
            messagebox.showinfo("Login Successful", f"Welcome, {username}! Role: {role}")
            self.root.destroy()  # Закрыть окно логина
            open_main_window(role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


def open_main_window(role):
    main_window = tk.Tk()
    main_window.title("Main Application")
    main_window.geometry("400x300")

    tk.Label(main_window, text=f"Logged in as: {role.capitalize()}").pack(pady=20)

    if role == "admin":
        tk.Button(main_window, text="Admin Features", command=lambda: print("Admin actions")).pack(pady=10)
    else:
        tk.Button(main_window, text="User Features", command=lambda: print("User actions")).pack(pady=10)

    main_window.mainloop()
