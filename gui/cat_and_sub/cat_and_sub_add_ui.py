import tkinter as tk
from tkinter import ttk, messagebox
from gui.utils_gui import show_frame
from category import load_categories, add_category, add_subcategory

type_display = {
    'income': 'Доходы',
    'expenses': 'Расходы'
    }

# Обратное соответствие:
type_reverse = {v: k for k, v in type_display.items()}

def create_add_ui(frame, data, back_callback):

    categories_wrapper = {"data": load_categories()}

    for widget in frame.winfo_children():
        widget.destroy()

    show_frame(frame, data)

    mode_var = tk.StringVar(value="category")  # Категория по умолчанию
    type_cat_var = tk.StringVar()
    type_sub_var = tk.StringVar()
    new_cat_var = tk.StringVar()
    parent_cat_var = tk.StringVar()
    new_sub_var = tk.StringVar()

    def handle_add():
        if mode_var.get() == "category":
            type_display_name = type_cat_var.get().strip()
            new_cat = new_cat_var.get().strip()

            if not type_display_name or not new_cat:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
                return

            type_key = type_reverse.get(type_display_name)
            if not type_key:
                messagebox.showerror("Ошибка", "Неверный тип транзакции.")
                return

            result = add_category(type_key, new_cat)
            if result["success"]:
                messagebox.showinfo("Успех", result["message"])
                categories_wrapper["data"] = load_categories()
                 # Очистка полей
                type_cat_var.set('')
                new_cat_var.set('')
                update_category_list(type_cat_var)
            else:
                messagebox.showerror("Ошибка", result["message"])

        else:  # mode == subcategory
            type_display_name = type_sub_var.get().strip()
            parent_cat = parent_cat_var.get().strip()
            new_sub = new_sub_var.get().strip()

            if not type_display_name or not parent_cat or not new_sub:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
                return

            type_key = type_reverse.get(type_display_name)
            if not type_key:
                messagebox.showerror("Ошибка", "Неверный тип транзакции.")
                return
            
            # === Вот здесь проверка на доходы ===
            if type_key == 'income':
                messagebox.showinfo("Недоступно", "Добавление подкатегорий к категориям доходов пока не поддерживается.")
                return

            result = add_subcategory(type_key, parent_cat, new_sub)
            if result["success"]:
                messagebox.showinfo("Успех", result["message"])
                categories_wrapper["data"] = load_categories()
                # Очистка полей
                type_sub_var.set('')
                parent_cat_var.set('')
                new_sub_var.set('')
                parent_cat_cb.config(state='disabled')
                update_category_list(type_sub_var)

            else:
                messagebox.showerror("Ошибка", result["message"])

    def update_category_list(type_):
        type_key = type_reverse.get(type_.get())
        if type_key:
            all_cats = categories_wrapper["data"].get(type_key, {})
            cats = list(all_cats.keys())

            parent_cat_cb.configure(values=cats)
            parent_cat_var.set('')
            return bool(cats)  # True, если список не пустой, иначе False
        return False

    def toggle_mode():
        if mode_var.get() == "category":
            type_cb_1.config(state='readonly')
            new_cat_entry.config(state="normal")
            set_state(sub_column_1, "disabled")
            set_state(sub_column_2, "disabled")

            # Сброс значений и списков подкатегорий
            type_sub_var.set("")
            parent_cat_var.set("")
            new_sub_var.set("")

            parent_cat_cb.configure(values=[])
        else:
            type_cb_2.config(state='readonly')
            new_sub_entry.config(state="normal")
            set_state(cat_column_1, "disabled")
            set_state(cat_column_2, "disabled")

            # Сброс значений и списков категорий
            type_cat_var.set("")
            new_cat_var.set("")

    def set_state(container, state):
        for child in container.winfo_children():
            try:
                # Не трогаем Label, у него нет параметра state
                if isinstance(child, tk.Label) or isinstance(child, ttk.Label):
                    continue
                child.configure(state=state)
            except:
                pass

    
    def on_type_selected(type_, cats_cb, event):
        cats_cb.config(state="readonly")
        update_category_list(type_)

    center_wrapper = tk.Frame(frame)
    center_wrapper.pack(expand=True, anchor='n')  # сверху, с отступом

    form = tk.Frame(center_wrapper)
    form.pack()

    # Настраиваем форму, чтобы колонка расширялась
    form.columnconfigure(0, weight=1)

    # === Добавление Категории ===
    cat_frame = tk.LabelFrame(form, text="Добавить категорию", padx=10, pady=10, width=700, height=130)
    cat_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    cat_frame.grid_propagate(False)

    # Обёртка для колонок
    cat_inner = tk.Frame(cat_frame)
    cat_inner.place(relx=0.5, rely=0.5, anchor='center')  # <-- Центрирование по вертикали и горизонтали

    cat_column_1 = tk.Frame(cat_inner)
    cat_column_1.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    cat_column_2 = tk.Frame(cat_inner)
    cat_column_2.grid(row=0, column=1, sticky='ew', padx=10, pady=5)

    tk.Label(cat_column_1, text="Тип транзакции:").grid(row=0, column=0, sticky='w', padx=0, pady=5)
    type_cb_1 = ttk.Combobox(cat_column_1, textvariable=type_cat_var, state="readonly")
    type_cb_1['values'] = list(type_display.values())
    type_cb_1.grid(row=0, column=1, padx=5)
    type_cb_1.bind("<<ComboboxSelected>>")

    tk.Label(cat_column_2, text="Новое название:").grid(row=0, column=0, sticky="w")
    new_cat_entry = ttk.Entry(cat_column_2, textvariable=new_cat_var)
    new_cat_entry.grid(row=0, column=1, padx=5)

    # === Добавление Подкатегории ===
    sub_frame = tk.LabelFrame(form, text="Добавить подкатегорию", padx=10, pady=10, width=700, height=160)
    sub_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
    sub_frame.grid_propagate(False)

    sub_inner = tk.Frame(sub_frame)
    sub_inner.place(relx=0.5, rely=0.5, anchor='center')  # <-- Центрирование по вертикали и горизонтали

    sub_column_1 = tk.Frame(sub_inner)
    sub_column_1.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    sub_column_2 = tk.Frame(sub_inner)
    sub_column_2.grid(row=0, column=1, sticky='ew', padx=10, pady=5)

    tk.Label(sub_column_1, text="Тип транзакции:").grid(row=0, column=0, sticky='w', padx=0, pady=5)
    type_cb_2 = ttk.Combobox(sub_column_1, textvariable=type_sub_var, state="disabled")
    type_cb_2['values'] = list(type_display.values())
    type_cb_2.grid(row=0, column=1, padx=5)
    type_cb_2.bind("<<ComboboxSelected>>", lambda e: on_type_selected(type_sub_var, parent_cat_cb, e))

    tk.Label(sub_column_1, text="Род. категория:").grid(row=1, column=0, sticky="w", pady=5)
    parent_cat_cb = ttk.Combobox(sub_column_1, textvariable=parent_cat_var, state="disabled")
    parent_cat_cb.grid(row=1, column=1, padx=5)
    parent_cat_cb.bind("<<ComboboxSelected>>")

    tk.Label(sub_column_2, text="Новое название:").grid(row=0, column=0, sticky="w")
    new_sub_entry = ttk.Entry(sub_column_2, textvariable=new_sub_var)
    new_sub_entry.grid(row=0, column=1, padx=5)

    # --- Переключатель ---
    radio_frame = tk.Frame(frame)
    radio_frame.pack(pady=10)
    tk.Radiobutton(radio_frame, text="Добавить категорию", variable=mode_var, value="category", command=toggle_mode).pack(side="left", padx=10)
    tk.Radiobutton(radio_frame, text="Добавить подкатегорию", variable=mode_var, value="subcategory", command=toggle_mode).pack(side="left", padx=10)

    # --- Кнопки ---
    buttons_frame = tk.Frame(frame)
    buttons_frame.pack(pady=20)
    ttk.Button(buttons_frame, text="Добавить", command=handle_add).pack(side="left", padx=10)
    ttk.Button(buttons_frame, text="Назад", command=back_callback).pack(side="left", padx=10)

    toggle_mode()