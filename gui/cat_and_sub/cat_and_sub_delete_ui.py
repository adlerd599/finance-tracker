import tkinter as tk
from tkinter import ttk, messagebox
from gui.utils_gui import show_frame
from app.category import load_categories, delete_category, delete_subcategory

type_display = {
    'income': 'Доходы',
    'expenses': 'Расходы'
    }

# Обратное соответствие:
type_reverse = {v: k for k, v in type_display.items()}

def create_delete_ui(frame, data, back_callback):

    categories_wrapper = {"data": load_categories()}

    for widget in frame.winfo_children():
        widget.destroy()

    show_frame(frame, data)

    mode_var = tk.StringVar(value="category")  # Категория по умолчанию
    type_cat_var = tk.StringVar()
    type_sub_var = tk.StringVar()
    category_var = tk.StringVar()
    parent_cat_var = tk.StringVar()
    subcategory_var = tk.StringVar()


    def handle_delete():
        
        if mode_var.get() == "category":
            
            type_display_name = type_cat_var.get().strip()
            category = category_var.get().strip()

            if not type_display_name or not category:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
                return

            type_key = type_reverse.get(type_display_name)
            if not type_key:
                messagebox.showerror("Ошибка", "Неверный тип транзакции.")
                return
            
            result = delete_category(type_key, category)
            if result["success"]:
                messagebox.showinfo("Успех", result["message"])
                categories_wrapper["data"] = load_categories()
                 # Очистка полей
                type_cat_var.set("")
                category_var.set("")

                old_cat_cb.configure(values=[])
                set_state(cat_column_1, "disabled")
                type_cb_1.config(state='readonly')

                update_category_list(type_cat_var, only_with_subcategories=False)
            else:
                messagebox.showerror("Ошибка", result["message"])
                 # Очистка полей
                type_cat_var.set("")
                category_var.set("")

                old_cat_cb.configure(values=[])
                set_state(cat_column_1, "disabled")
                type_cb_1.config(state='readonly')

                update_category_list(type_cat_var, only_with_subcategories=False)

        else:  # mode == subcategory
            type_display_name = type_sub_var.get().strip()
            parent_cat = parent_cat_var.get().strip()
            subcategory = subcategory_var.get().strip()

            if not type_display_name or not parent_cat or not subcategory:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
                return

            type_key = type_reverse.get(type_display_name)
            if not type_key:
                messagebox.showerror("Ошибка", "Неверный тип транзакции.")
                return

            result = delete_subcategory(type_key, parent_cat, subcategory)
            
            if result is None:
                return

            if result["success"]:
                messagebox.showinfo("Успех", result["message"])
                categories_wrapper["data"] = load_categories()
                # Очистка полей
                type_sub_var.set("")
                parent_cat_var.set("")
                subcategory_var.set("")
                set_state(sub_column_1, "disabled")
                type_cb_2.config(state='readonly')

                parent_cat_cb.configure(values=[])
                old_sub_cb.configure(values=[])
                update_category_list(type_sub_var, only_with_subcategories=True)
            else:
                messagebox.showerror("Ошибка", result["message"])
                # Очистка полей
                type_sub_var.set("")
                parent_cat_var.set("")
                subcategory_var.set("")
                set_state(sub_column_1, "disabled")
                type_cb_2.config(state='readonly')

                parent_cat_cb.configure(values=[])
                old_sub_cb.configure(values=[])
                update_category_list(type_sub_var, only_with_subcategories=True)

    def update_category_list(type_, only_with_subcategories=False):
        type_key = type_reverse.get(type_.get())
        if type_key:
            all_cats = categories_wrapper["data"].get(type_key, {})
            
            if only_with_subcategories:
                # Фильтруем категории, у которых есть хотя бы одна подкатегория
                cats = [cat for cat, subs in all_cats.items() if subs]
            else:
                # Все категории
                cats = list(all_cats.keys())

            old_cat_cb.configure(values=cats)
            parent_cat_cb.configure(values=cats)
            category_var.set('')
            parent_cat_var.set('')
            old_sub_cb.configure(values=[])
            return bool(cats)  # True, если список не пустой, иначе False
        return False

    def update_subcategory_list(event=None):
        type_key = type_reverse.get(type_sub_var.get())
        parent_cat = parent_cat_var.get()
        if type_key and parent_cat:
            subs = categories_wrapper["data"].get(type_key, {}).get(parent_cat, [])
            old_sub_cb.configure(values=subs)
            # parent_cat_var.set('')
            subcategory_var.set('')

    def toggle_mode():
        if mode_var.get() == "category":
            type_cb_1.config(state='readonly')
            set_state(sub_column_1, "disabled")

            # Сброс значений и списков подкатегорий
            type_sub_var.set("")
            parent_cat_var.set("")
            subcategory_var.set("")

            parent_cat_cb.configure(values=[])
            old_sub_cb.configure(values=[])
        else:
            type_cb_2.config(state='readonly')
            set_state(cat_column_1, "disabled")

            # Сброс значений и списков категорий
            type_cat_var.set("")
            category_var.set("")

            old_cat_cb.configure(values=[])

    def set_state(container, state):
        for child in container.winfo_children():
            try:
                # Не трогаем Label, у него нет параметра state
                if isinstance(child, tk.Label) or isinstance(child, ttk.Label):
                    continue
                child.configure(state=state)
            except:
                pass

    
    def on_type_selected(type_, cats_cb, bool_, event):
        if not update_category_list(type_, bool_):
            messagebox.showinfo("Нет категорий", "Нет категорий с подкатегориями для выбранного типа.")
            cats_cb.config(state="disabled")
            old_sub_cb.config(state="disabled")
        else:
            cats_cb.config(state="readonly")
            old_sub_cb.config(state="disabled")
    
    def on_cat_selected(sub_cb,event):
        sub_cb.config(state='readonly')
        update_subcategory_list()

    center_wrapper = tk.Frame(frame)
    center_wrapper.pack(expand=True, anchor='n')  # сверху, с отступом

    form = tk.Frame(center_wrapper)
    form.pack()

    # Настраиваем форму, чтобы колонка расширялась
    form.columnconfigure(0, weight=1)

    # --- Категория ---
    cat_frame = tk.LabelFrame(form, text="Удалить категорию", padx=10, pady=10, width=700, height=130)
    cat_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    cat_frame.grid_propagate(False)
    cat_frame.columnconfigure(0, weight=1)  # Чтобы содержимое могло центрироваться

    # Обёртка для колонок
    cat_inner = tk.Frame(cat_frame)
    cat_inner.place(relx=0.5, rely=0.5, anchor='center')  # <-- Центрирование по вертикали и горизонтали

    cat_column_1 = tk.Frame(cat_inner)
    cat_column_1.grid(row=0, column=0, pady=5)

    tk.Label(cat_column_1, text="Тип транзакции:").grid(row=0, column=0, sticky='w', padx=0, pady=5)
    type_cb_1 = ttk.Combobox(cat_column_1, textvariable=type_cat_var, state="readonly")
    type_cb_1['values'] = list(type_display.values())
    type_cb_1.grid(row=0, column=1, padx=5)
    type_cb_1.bind("<<ComboboxSelected>>", lambda e: on_type_selected(type_cat_var, old_cat_cb, False, e))

    tk.Label(cat_column_1, text="Категория:").grid(row=1, column=0, sticky="w", pady=5)
    old_cat_cb = ttk.Combobox(cat_column_1, textvariable=category_var, state="disabled")
    old_cat_cb.grid(row=1, column=1, padx=5)

    # --- Подкатегория ---
    sub_frame = tk.LabelFrame(form, text="Удалить подкатегорию", padx=10, pady=10, width=700, height=160)
    sub_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
    sub_frame.grid_propagate(False)
    sub_frame.columnconfigure(0, weight=1)

    # Обёртка для колонок
    sub_inner = tk.Frame(sub_frame)
    sub_inner.place(relx=0.5, rely=0.5, anchor='center')  # <-- Центрирование по вертикали и горизонтали

    sub_column_1 = tk.Frame(sub_inner)
    sub_column_1.grid(row=0, column=0, pady=5)
    
    tk.Label(sub_column_1, text="Тип транзакции:").grid(row=0, column=0, sticky='w', padx=0, pady=5)
    type_cb_2 = ttk.Combobox(sub_column_1, textvariable=type_sub_var, state="disabled")
    type_cb_2['values'] = list(type_display.values())
    type_cb_2.grid(row=0, column=1, padx=5)
    type_cb_2.bind("<<ComboboxSelected>>", lambda e: on_type_selected(type_sub_var, parent_cat_cb, True, e))

    tk.Label(sub_column_1, text="Род. категория:").grid(row=1, column=0, sticky="w", pady=5)
    parent_cat_cb = ttk.Combobox(sub_column_1, textvariable=parent_cat_var, state="disabled")
    parent_cat_cb.grid(row=1, column=1, padx=5)
    parent_cat_cb.bind("<<ComboboxSelected>>", lambda e: on_cat_selected(old_sub_cb, e))

    tk.Label(sub_column_1, text="Подкатегория:").grid(row=2, column=0, sticky="w", pady=5)
    old_sub_cb = ttk.Combobox(sub_column_1, textvariable=subcategory_var, state="disabled")
    old_sub_cb.grid(row=2, column=1, padx=5)

    # --- Переключатель ---
    radio_frame = tk.Frame(frame)
    radio_frame.pack(pady=10)
    tk.Radiobutton(radio_frame, text="Удалить категорию", variable=mode_var, value="category", command=toggle_mode).pack(side="left", padx=10)
    tk.Radiobutton(radio_frame, text="Удалить подкатегорию", variable=mode_var, value="subcategory", command=toggle_mode).pack(side="left", padx=10)

    # --- Кнопки ---
    buttons_frame = tk.Frame(frame)
    buttons_frame.pack(pady=20)
    ttk.Button(buttons_frame, text="Удалить", command = handle_delete).pack(side="left", padx=10)
    ttk.Button(buttons_frame, text="Назад", command=back_callback).pack(side="left", padx=10)

    toggle_mode()