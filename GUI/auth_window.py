import tkinter as tk
from tkinter import messagebox, ttk
from GUI.admin_features import AdminFeaturesWindow
from GUI.reference_window import ReferencesWindowAdmin
from GUI.user_features import UserFeaturesWindow


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


def open_admin_features(parent):
    table_selection_window = tk.Toplevel(parent)
    table_selection_window.title("Select Table to Manage")
    table_selection_window.geometry("300x200")

    tk.Label(table_selection_window,
             text="Select a table to manage:",
             font=("Arial", 14)).pack(pady=20)

    tables = ["people", "groups", "subjects", "marks"]
    selected_table = tk.StringVar(value=tables[0])

    table_dropdown = ttk.Combobox(table_selection_window,
                                  values=tables,
                                  textvariable=selected_table,
                                  state="readonly")
    table_dropdown.pack(pady=10)

    # Кнопка подтверждения выбора
    tk.Button(
        table_selection_window,
        text="Open",
        command=lambda: open_table_window(parent, selected_table.get(), table_selection_window)
    ).pack(pady=10)

    # Кнопка закрытия окна
    tk.Button(
        table_selection_window,
        text="Cancel",
        command=table_selection_window.destroy
    ).pack(pady=5)


def open_user_features(parent):
    user_window = tk.Toplevel(parent)
    user_window.title("User Features")
    user_window.geometry("400x300")
    tk.Label(user_window, text="User Features Window", font=("Arial", 14)).pack(pady=20)
    tk.Button(user_window, text="Close", command=user_window.destroy).pack(pady=20)


def open_main_window(role):
    main_window = tk.Tk()
    main_window.title("Main Application")
    main_window.geometry("400x300")

    tk.Label(main_window, text=f"Logged in as: {role.capitalize()}").pack(pady=20)

    if role == "admin":
        tk.Button(main_window, text="Admin Features", command=lambda: open_admin_features(main_window)).pack(pady=10)
    else:
        tk.Button(main_window, text="User Features", command=lambda: open_user_features(main_window)).pack(pady=10)

    main_window.mainloop()


def open_table_window(parent, table_name, selection_window):
    selection_window.destroy()  # Закрытие окна выбора
    ReferencesWindowAdmin(parent, table_name)
