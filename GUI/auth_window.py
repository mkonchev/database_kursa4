import tkinter as tk
from tkinter import messagebox


def login():
    username = username_entry.get()
    password = password_entry.get()

    # Временно проверяем жестко заданный пароль
    if username == "admin" and password == "password":
        messagebox.showinfo("Success", "Login successful!")
        root.destroy()  # Закрыть окно авторизации
        open_main_window()  # Открыть главное окно
    else:
        messagebox.showerror("Error", "Something went wrong(((")


def open_main_window():
    main_window = tk.Tk()
    main_window.title("Main Window")
    tk.Label(main_window, text="Hello!").pack()
    main_window.mainloop()


root = tk.Tk()
root.title("Login")

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=login).pack()

root.mainloop()
