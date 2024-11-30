if __name__ == "__main__":
    from Connection.DBConnection import DatabaseConnection
    from Authorization.Check_password import Authenticator
    from GUI.auth_window import LoginApp
    import tkinter as tk

    db = DatabaseConnection("Connection/db_config.ini")
    authenticator = Authenticator("Connection/db_config.ini")
    root = tk.Tk()
    app = LoginApp(root, authenticator)
    root.mainloop()

