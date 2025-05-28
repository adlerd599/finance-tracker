import tkinter as tk
from tkinter import ttk

def show_filtered_transactions(transactions, frame=None):
    if frame is None:
        frame = tk.Toplevel()
        frame.title("Список транзакций")
        frame.geometry("1000x700")

    for widget in frame.winfo_children():
        widget.destroy()

    # Заголовок
    tk.Label(frame, text="Список транзакций", font=("Arial", 14)).pack(pady=10)

    # Обертка под Treeview + скроллбар
    tree_frame = tk.Frame(frame)
    tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

    columns = ("id","amount", "type", "category", "subcategory", "description", "optional", "date")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

    # Заголовки столбцов
    tree.heading("id", text="ID")
    tree.heading("amount", text="Сумма")
    tree.heading("type", text="Тип")
    tree.heading("category", text="Категория")
    tree.heading("subcategory", text="Подкатегория")
    tree.heading("description", text="Описание")
    tree.heading("optional", text="Необязательная")
    tree.heading("date", text="Дата")

    # Настройки ширины (можно подстроить)
    tree.column("id", width=80, anchor="center")
    tree.column("amount", width=80, anchor="center")
    tree.column("type", width=100, anchor="center")
    tree.column("category", width=100, anchor="center")
    tree.column("subcategory", width=100, anchor="center")
    tree.column("description", width=100, anchor="center")
    tree.column("optional", width=100, anchor="center")
    tree.column("date", width=100, anchor="center")

    # Прокрутка
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    tree.pack(fill='both', expand=True)

    style = ttk.Style()
    style.configure("Treeview", rowheight=25)  # увеличим высоту строк
    style.map("Treeview", background=[("selected", "#d1e0ff")])

    # Чередование фона строк
    tree.tag_configure('oddrow', background='#f9f9f9')
    tree.tag_configure('evenrow', background='#ffffff')

    for index, tx in enumerate(transactions):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert('', 'end', values=(
            tx.get("id", ""),
            f'{tx.get("amount", 0):.2f}',
            "Доход" if tx.get("type_") == "income" else "Расход",
            tx.get("category", ""),
            tx.get("subcategory", "") if tx.get("type_") == "expenses" else "-",
            tx.get("description", ""),
            "Да" if tx.get("optional") else "Нет",
            tx.get("date", ""),
        ), tags=(tag,))

    # Кнопка "Назад"
    ttk.Button(frame, text="Назад", command=lambda: frame.pack_forget() if hasattr(frame, 'pack') else frame.destroy()).pack(pady=10)