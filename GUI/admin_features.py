import tkinter as tk
from tkinter import ttk, messagebox


class AdminFeaturesWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Admin Features")
        self.window.geometry("400x300")

        # Заголовок окна
        tk.Label(self.window, text="Admin Features", font=("Arial", 14)).pack(pady=20)

        # Кнопка для открытия справочников
        tk.Button(self.window, text="Manage Users", command=self.manage_users).pack(pady=10)
        tk.Button(self.window, text="Add New Record", command=self.add_new_record).pack(pady=10)

        # Закрытие окна
        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=20)

    def manage_users(self):
        messagebox.showinfo("Manage Users", "Here you can manage users (add, edit, delete).")
        # Логика для управления пользователями

    def add_new_record(self):
        messagebox.showinfo("Add New Record", "Here you can add a new record.")
        # Логика для добавления новых записей
