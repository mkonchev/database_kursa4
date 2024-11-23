import tkinter as tk
from tkinter import ttk, messagebox


class UserFeaturesWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("User Features")
        self.window.geometry("400x300")

        # Заголовок окна
        tk.Label(self.window, text="User Features", font=("Arial", 14)).pack(pady=20)

        # Кнопка для просмотра данных
        tk.Button(self.window, text="View Data", command=self.view_data).pack(pady=10)

        # Закрытие окна
        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=20)

    def view_data(self):
        messagebox.showinfo("View Data", "Here you can view data relevant to your role.")
        # Логика для просмотра данных
