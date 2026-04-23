import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data = []
        self.load_data()

        # --- Поля ввода ---
        ttk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # --- Кнопка добавления ---
        ttk.Button(root, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # --- Таблица расходов ---
        self.tree = ttk.Treeview(root, columns=("Сумма", "Категория", "Дата"), show="headings")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # --- Фильтры ---
        ttk.Label(root, text="Фильтр по категории:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_category = ttk.Combobox(root, values=self.get_categories())
        self.filter_category.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(root, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=7, column=0, columnspan=2, pady=5)

        # --- Период для суммы ---
        ttk.Label(root, text="Период (ГГГГ-ММ-ДД):").grid(row=8, column=0, padx=5, pady=5)
        self.period_start = ttk.Entry(root)
        self.period_start.grid(row=8, column=1, padx=5, pady=5)

        ttk.Label(root, text="по").grid(row=9, column=0, padx=5)

        self.period_end = ttk.Entry(root)
        self.period_end.grid(row=9, column=1, padx=5)

        ttk.Button(root, text="Сумма за период", command=self.sum_for_period).grid(row=10, column=0, columnspan=2, pady=5)

        # --- Кнопки сохранения/загрузки ---
        ttk.Button(root, text="Сохранить в JSON", command=self.save_data).grid(row=11, column=0, pady=5)
        ttk.Button(root, text="Загрузить из JSON", command=self.load_data_gui).grid(row=11, column=1, pady=5)

        # Заполнение таблицы
        self.update_tree()

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not self.validate_input(amount, date):
            return

        self.data.append({
            "amount": float(amount),
            "category": category,
            "date": date
        })

        self.update_tree()
        self.clear_entries()

    def validate_input(self, amount, date):
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
                return False
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ввод! Проверьте сумму и дату.")
            return False

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.data:
            self.tree.insert("", "end", values=(item["amount"], item["category"], item["date"]))

    def get_categories(self):
        return sorted(set([x["category"] for x in self.data] + [""]))

    def apply_filter(self):
        category = self.filter_category.get()
        date = self.filter_date.get()

        filtered = self.data

        if category:
            filtered = [x for x in filtered if x["category"] == category]

        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                filtered = [x for x in filtered if x["date"] == date]
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат даты для фильтра!")
                return

        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in filtered:
            self.tree.insert("", "end", values=(item["amount"], item["category"], item["date"]))

    def sum_for_period(self):
        start = self.period_start.get()
        end = self.period_end.get()

        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            total = sum(x["amount"] for x in self.data if start_date <= datetime.strptime(x["date"], "%Y-%m-%d") <= end_date)
            messagebox.showinfo("Сумма за период", f"Сумма расходов: {total:.2f} руб.")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты периода!")

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
                self.update_tree()
                self.filter_category["values"] = self.get_categories()
                return True
        except FileNotFoundError:
            return False

    def load_data_gui(self):
        if self.load_data():
            messagebox.# Expense Tracker — полный проект
