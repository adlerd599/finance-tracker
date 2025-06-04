import tkinter as tk
from tkinter import ttk

def show_filtered_transactions(transactions, sort_by):
    frame = tk.Toplevel()
    frame.title("Список транзакций")
    frame.geometry("1000x700")

    # --- Центрирование окна ---
    frame.update_idletasks()  # Нужно, чтобы размеры окна точно обновились
    screen_width = frame.winfo_screenwidth()
    screen_height = frame.winfo_screenheight()

    width = 1000
    height = 700

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    frame.geometry(f"{width}x{height}+{x}+{y}")

    for widget in frame.winfo_children():
        widget.destroy()

    # Заголовок
    tk.Label(frame, text=f"Список | Фильтрация: {sort_by}", font=("Helvetica", 12)).pack(pady=10)

    # Обертка под Treeview + скроллбар
    tree_frame = tk.Frame(frame)
    tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

    columns = ("#","id","amount", "type", "category", "subcategory", "description", "optional", "date")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

    # Заголовки столбцов
    tree.heading("#", text="#")
    tree.heading("id", text="ID")
    tree.heading("amount", text="Сумма")
    tree.heading("type", text="Тип")
    tree.heading("category", text="Категория")
    tree.heading("subcategory", text="Подкатегория")
    tree.heading("description", text="Описание")
    tree.heading("optional", text="Необязательная")
    tree.heading("date", text="Дата")

    # Настройки ширины (можно подстроить)
    tree.column("#", width=40, anchor="center")
    tree.column("id", width=80, anchor="center")
    tree.column("amount", width=80, anchor="center")
    tree.column("type", width=100, anchor="center")
    tree.column("category", width=100, anchor="center")
    tree.column("subcategory", width=100, anchor="center")
    tree.column("description", width=160, anchor="center")
    tree.column("optional", width=40, anchor="center")
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
        number = index + 1
        tree.insert('', 'end', values=(
            number, 
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
    ttk.Button(frame, text="Закрыть", command=lambda: frame.pack_forget() if hasattr(frame, 'pack') else frame.destroy()).pack(pady=10)