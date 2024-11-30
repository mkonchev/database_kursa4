import tkinter as tk
from tkinter import ttk, messagebox
from Connection.DBConnection import DatabaseConnection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ReferencesWindowUser:
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

            tk.Button(button_frame, text="Exit", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="AVG value", command=self.show_analysis_dialog).pack(side=tk.LEFT, padx=5)

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

    def show_analysis_dialog(self):
        """Открывает окно для анализа данных."""
        analysis_window = tk.Toplevel(self.window)
        analysis_window.title("Analyze Data")
        analysis_window.geometry("600x400")

        # Фильтры
        filter_frame = tk.LabelFrame(analysis_window, text="Filters")
        filter_frame.pack(fill=tk.X, padx=10, pady=10)

        filter_options = ["Year", "Student", "Group", "Subject", "Teacher"]
        filter_var = tk.StringVar(value="Year")
        tk.Label(filter_frame, text="Filter By:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        filter_menu = ttk.Combobox(filter_frame, textvariable=filter_var, values=filter_options)
        filter_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Start Year:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        start_year = tk.StringVar(value="")
        tk.Entry(filter_frame, textvariable=start_year).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="End Year:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        end_year = tk.StringVar(value="")
        tk.Entry(filter_frame, textvariable=end_year).grid(row=2, column=1, padx=5, pady=5)

        # Кнопки анализа
        button_frame = tk.Frame(analysis_window)
        button_frame.pack(fill=tk.X, pady=10)

        tk.Button(button_frame, text="Show Table",
                  command=lambda: self.show_analysis_table(filter_var.get(),
                                                           start_year.get(),
                                                           end_year.get())).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Show Graph",
                  command=lambda: self.show_analysis_graph(filter_var.get(),
                                                           start_year.get(),
                                                           end_year.get())).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Close", command=analysis_window.destroy).pack(side=tk.LEFT, padx=5)

    def show_analysis_table(self, filter_by, start_year, end_year):
        """Показывает результаты анализа в табличной форме."""
        db = DatabaseConnection()
        db.connect()

        try:
            cursor = db.connection.cursor()

            if filter_by == "Year":
                str_ = f"""CALL get_average_grade_by_year_proc({start_year}, {end_year})"""
                cursor.execute(str_)
            elif filter_by == "Student":
                str_ = f"""CALL get_average_grade_by_student_proc({start_year}, {end_year})"""
                cursor.execute(str_)
            elif filter_by == "Group":
                str_ = f"""CALL get_average_grade_by_group_proc({start_year}, {end_year})"""
                cursor.execute(str_)
            elif filter_by == "Subject":
                str_ = f"""CALL get_average_grade_by_subject_proc({start_year}, {end_year})"""
                cursor.execute(str_)
            elif filter_by == "Teacher":
                str_ = f"""CALL get_average_grade_by_teacher_proc({start_year}, {end_year})"""
                cursor.execute(str_)
            else:
                raise ValueError("Invalid filter")

            cursor.execute("SELECT * FROM temp_average_grades")
            results = cursor.fetchall()

            # Создание окна с таблицей
            table_window = tk.Toplevel(self.window)
            table_window.title("Analysis Results")
            table_window.geometry("400x300")

            table = ttk.Treeview(table_window, columns=("Filter", "Average Grade"), show="headings")
            table.heading("Filter", text=filter_by.capitalize())
            table.heading("Average Grade", text="Average Grade")
            table.pack(fill=tk.BOTH, expand=True)

            for row in results:
                table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze data: {e}")
        finally:
            db.close()

    def show_analysis_graph(self, filter_by, start_year, end_year):
        """Показывает результаты анализа в графическом виде."""
        db = DatabaseConnection()
        db.connect()

        try:
            cursor = db.connection.cursor()

            if filter_by == "Year":
                str_ = f"""CALL get_average_grade_by_year_proc({start_year}, {end_year})"""
                cursor.execute(str_)
            elif filter_by == "Student":
                str_ = f"""CALL get_average_grade_by_student_proc({start_year}, {end_year})"""
                cursor.execute(str_)
            elif filter_by == "Group":
                str_ = f"""CALL get_average_grade_by_group_proc({start_year}, {end_year})"""
                cursor.execute(str_)
            elif filter_by == "Subject":
                str_ = f"""CALL get_average_grade_by_subject_proc({start_year}, {end_year})"""
                cursor.execute(str_)
            elif filter_by == "Teacher":
                str_ = f"""CALL get_average_grade_by_teacher_proc({start_year}, {end_year})"""
                cursor.execute(str_)
            else:
                raise ValueError("Invalid filter")

            cursor.execute("SELECT * FROM temp_average_grades")
            results = cursor.fetchall()

            labels = [row[0] for row in results]
            values = [row[1] for row in results]

            fig, ax = plt.subplots(figsize=(10, 6))
            plt.bar(labels, values, color="skyblue")
            plt.xlabel(filter_by.capitalize())
            plt.ylabel("Average Grade")
            plt.title(f"Average Grade by {filter_by.capitalize()}")
            plt.xticks(rotation=45)
            plt.tight_layout()

            graph_window = tk.Toplevel(self.window)  # новое окно
            graph_window.title(f"{filter_by.capitalize()} Analysis Graph")
            graph_window.geometry("800x600")

            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze data: {e}")
        finally:
            db.close()
