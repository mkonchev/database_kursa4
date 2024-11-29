import tkinter as tk
from tkinter import ttk, messagebox
from Connection.DBConnection import DatabaseConnection
from GUI.record_form import RecordForm


class ReferencesWindowAdmin:
    def __init__(self, parent, table_name):
        self.table_name = table_name  # Имя таблицы
        self.window = tk.Toplevel(parent)
        self.window.title(f"Manage {table_name.capitalize()}")
        self.window.geometry("800x400")

        # Подключение к базе данных
        db = DatabaseConnection()
        db.connect()

        try:
            cursor = db.connection.cursor()

            # Получение структуры таблицы (названия столбцов)
            cursor.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position;",
                (table_name,))
            self.columns = [col[0] for col in cursor.fetchall()]

            # Создание Treeview с динамическими столбцами
            self.tree = ttk.Treeview(self.window, columns=self.columns, show="headings")
            for col in self.columns:
                self.tree.heading(col, text=col.capitalize())
                self.tree.column(col, anchor="center", width=100)  # Установить ширину столбцов

            self.tree.pack(fill=tk.BOTH, expand=True)

            # Кнопки управления
            button_frame = tk.Frame(self.window)
            button_frame.pack(fill=tk.X, pady=10)

            tk.Button(button_frame, text="Add", command=self.add_record).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Edit", command=self.edit_record).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Delete", command=self.delete_record).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Refresh", command=self.load_data).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Exit", command=self.window.destroy).pack(side=tk.LEFT, padx=5)

            self.load_data()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load table structure: {e}")
        finally:
            db.close()

    def load_data(self):
        """Загрузка данных из таблицы в Treeview."""
        self.tree.delete(*self.tree.get_children())  # Очистка текущих данных

        db = DatabaseConnection()
        db.connect()

        try:
            cursor = db.connection.cursor()
            query = f"SELECT * FROM {self.table_name};"
            cursor.execute(query)
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
        finally:
            db.close()

    def add_record(self):
        """Добавление записи"""
        RecordForm(
            parent=self.window,
            table_name=self.table_name,
            columns=[col for col in self.columns if col != "id"],
            mode="add",
            on_close=self.load_data
        )

    def edit_record(self):
        """Редактирование записи"""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "No record selected!")
            return
        # Получение данных о выбранной записи
        record_data = self.tree.item(selected_item)["values"]
        if not record_data:
            messagebox.showwarning("Warning", "Could not fetch record data!")
            return
        record_dict = {col: val for col, val in zip(self.columns, record_data)}

        # Открытие формы редактирования
        RecordForm(
            parent=self.window,
            table_name=self.table_name,
            columns=[col for col in self.columns if col != "id"],  # Указываем все столбцы кроме `id`
            mode="edit",
            record_data=record_dict,  # Передаём данные записи для редактирования
            on_close=self.load_data
        )

    def delete_record(self):
        """Удаление записи"""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "No record selected!")
            return

        record_id = self.tree.item(selected_item)["values"][0]  # Предполагаем, что первый столбец - ID
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this record?")
        if not confirm:
            return

        db = DatabaseConnection()
        db.connect()

        try:
            cursor = db.connection.cursor()
            query = f"DELETE FROM {self.table_name} WHERE id = %s;"
            cursor.execute(query, (record_id,))
            db.connection.commit()
            messagebox.showinfo("Success", "Record deleted successfully!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record: {e}")
        finally:
            db.close()
