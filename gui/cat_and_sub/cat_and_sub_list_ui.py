import tkinter as tk
from tkinter import ttk
from app.category import load_categories
from gui.utils_gui import show_frame

def create_cat_and_sub_list(frame, data, back_callback):

    for widget in frame.winfo_children():
            widget.destroy()

    show_frame(frame, data)

    # Загрузка категорий
    categories = load_categories()

    # Заголовок
    tk.Label(frame, text="Категории и подкатегории:", font=("Helvetica", 12)).pack(pady=10)

    # Контейнер для двух деревьев
    trees_frame = tk.Frame(frame)
    trees_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ======= Доходы =======
    income_tree = ttk.Treeview(trees_frame)
    income_tree.heading("#0", text="Доходы", anchor="center")

    for category, subcats in categories.get("income", {}).items():
        cat_id = income_tree.insert("", "end", text=category, open=False)
        for sub in subcats:
            income_tree.insert(cat_id, "end", text=sub)

    income_tree.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

    # ======= Расходы =======
    expense_tree = ttk.Treeview(trees_frame)
    expense_tree.heading("#0", text="Расходы", anchor="center")

    for category, subcats in categories.get("expenses", {}).items():
        cat_id = expense_tree.insert("", "end", text=category, open=False)
        for sub in subcats:
            expense_tree.insert(cat_id, "end", text=sub)

    expense_tree.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

    # Убираем синие выделения
    style = ttk.Style()
    style.map("Treeview",
        background=[("selected", "white")],  # белый фон при выделении
        foreground=[("selected", "black")]   # чёрный текст при выделении
    )

    # Настройки масштабирования
    trees_frame.columnconfigure(0, weight=1)
    trees_frame.columnconfigure(1, weight=1)
    trees_frame.rowconfigure(0, weight=1)

    ttk.Button(frame, text="Назад", command=back_callback).pack(pady=5)