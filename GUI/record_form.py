import configparser
import tkinter as tk
from tkinter import ttk, messagebox

import psycopg2


class RecordForm:
    def __init__(self, parent, table_name, columns, mode, record_data=None, on_close=None):
        """Форма для добавления или редактирования записей."""
        self.table_name = table_name
        self.columns = columns
        self.mode = mode
        self.record_data = record_data if isinstance(record_data, dict) else {}
        self.on_close = on_close

        # Создаём окно формы
        self.window = tk.Toplevel(parent)
        self.window.title("Add Record" if mode == "add" else "Edit Record")
        self.window.geometry("400x300")

        self.entries = {}

        # Создание полей ввода
        for i, column in enumerate(columns):
            tk.Label(self.window, text=column.capitalize()).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(self.window)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            # Заполняем текущими значениями в режиме редактирования
            if mode == "edit" and self.record_data:
                entry.insert(0, record_data.get(column, ""))

            self.entries[column] = entry

        # Кнопки "Save" и "Cancel"
        tk.Button(self.window, text="Save", command=self.save).grid(row=len(columns), column=0, padx=10, pady=10)
        tk.Button(self.window, text="Cancel", command=self.window.destroy).grid(row=len(columns), column=1, padx=10,
                                                                                pady=10)

    def save(self):
        """Сохранение данных в БД."""
        data = {column: entry.get() for column, entry in self.entries.items()}
        if "id" in data:
            del data["id"]
        try:
            # Формирование SQL-запроса
            if self.mode == "add":
                if "id" in data:
                    del data["id"]
                placeholders = ", ".join(["%s"] * len(data))
                query = f"INSERT INTO {self.table_name} ({', '.join(data.keys())}) VALUES ({placeholders})"
                params = tuple(data.values())
            elif self.mode == "edit":
                if "id" in data:
                    del data["id"]
                if "id" not in self.record_data:
                    raise ValueError("ID is missing in record_data for edit operation")
                set_clause = ", ".join([f"{col} = %s" for col in data.keys()])
                print('passssssss')
                query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"
                params = tuple(data.values()) + (self.record_data["id"],)
                print(f"Executing query: {query} with params: {params}")

            # Подключение и выполнение запроса
            db_config = self.get_db_config()  # Получение параметров конфигурации
            print(f"Connecting to database with config: {db_config}")

            connection = psycopg2.connect(**db_config)
            cursor = connection.cursor()

            cursor.execute(query, params)
            connection.commit()
            self.window.destroy()

            if self.on_close:
                self.on_close()
        except Exception as e:
            print(f"Error occurred during query execution: {e}")
            messagebox.showerror("Error", f"Failed to save record: {e}")
        finally:
            if 'connection' in locals() and connection:
                connection.close()

    def get_db_config(self):
        config = configparser.ConfigParser()
        config.read('Connection/db_config.ini')  # Путь к вашему файлу конфигурации

        return {
            'host': config.get('database', 'host'),
            'port': config.get('database', 'port'),
            'user': config.get('database', 'user'),
            'password': config.get('database', 'password'),
            'database': config.get('database', 'database'),
        }
