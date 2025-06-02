import tkinter as tk
from tkinter import ttk, messagebox
from app.transaction import add_transaction
from app.category import load_categories
from app.utils import validate_date
from gui.utils_gui import show_frame
from .utils_gui import validate_amount_input, validate_date_input, auto_format_date_input, remove_combobox_selection

type_display = {
    'income': 'Доходы',
    'expenses': 'Расходы'
}

# Обратное соответствие:
type_reverse = {v: k for k, v in type_display.items()}

def create_add_transaction_ui(frame, data, back_callback):
    categories = load_categories()

    for widget in frame.winfo_children():
            widget.destroy()

    show_frame(frame, data)

    type_var = tk.StringVar()
    category_var = tk.StringVar()
    subcategory_var = tk.StringVar()
    amount_var = tk.StringVar()
    description_var = tk.StringVar()
    date_var = tk.StringVar()
    optional_var = tk.BooleanVar()

    def reset_form_fields():
        amount_var.set("")
        description_var.set("")
        date_var.set("")
        type_var.set("")
        category_var.set("")
        subcategory_var.set("")
        optional_var.set(False)

        category_cb['values'] = []
        subcategory_cb['values'] = []

        subcategory_label.grid_forget()
        subcategory_cb.grid_forget()
        optional_cb.grid_forget()

    def handle_back():
        reset_form_fields()
        back_callback()

    def update_categories(*args):
        categories_data = load_categories()
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')  # 'income' или 'expenses'
        categories = list(categories_data.get(type_, {}).keys())
        category_cb['values'] = categories
        category_var.set('')
        subcategory_cb['values'] = []
        subcategory_var.set('')
        toggle_expense_fields()

    def update_subcategories(*args):
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')
        category = category_var.get()
        subcategories = categories.get(type_, {}).get(category, [])

        subcategory_cb['values'] = subcategories
        subcategory_var.set('')

            # Делаем список неактивным, если подкатегорий нет
        if subcategories:
            subcategory_cb.config(state='readonly')
        else:
            subcategory_cb.config(state='disabled')

    # Появление подкатегорий
    def toggle_expense_fields():
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')

        if type_ == 'expenses':
            subcategory_label.grid(row=2, column=2, sticky='w', padx=0, pady=5)
            subcategory_cb.grid(row=2, column=3, padx= 0, pady=5)
            optional_cb.grid(row=3, column=2, columnspan=3, sticky='w', padx= 0, pady=5)
            subcategory_cb.config(state='readonly' if subcategory_cb['values'] else 'disabled')
        else:
            subcategory_label.grid_forget()
            subcategory_cb.grid_forget()
            optional_cb.grid_forget()
            optional_var.set(False)

    def save_transaction():
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')
        categories_data = load_categories()
        category = category_var.get()
        date_str = date_var.get()

        if not amount_var.get().strip():
            messagebox.showerror("Ошибка", "Поле 'Сумма' обязательно для заполнения.")
            return
        if not type_var.get().strip():
            messagebox.showerror("Ошибка", "Поле 'Тип' обязательно для заполнения.")
            return
        if not category_var.get().strip():
            messagebox.showerror("Ошибка", "Поле 'Категория' обязательно для заполнения.")
            return
        if type_ == 'expenses':
            subcategories = categories_data.get(type_, {}).get(category, [])
            if subcategories and not subcategory_var.get().strip():
                messagebox.showerror("Ошибка", "Поле 'Подкатегория' обязательно для заполнения.")
                return
            
        # Проверка даты
        validated_date = validate_date(date_str)
        if date_str.strip():
            if not validated_date:
                messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
                return
    
        try:
            amount = float(amount_var.get())
            type_displayed = type_var.get()
            type_ = type_reverse.get(type_displayed, '')
            category = category_var.get()
            subcategory = subcategory_var.get() if type_ == 'expenses' else ''
            description = description_var.get()
            date_str = validated_date
            optional = optional_var.get() if type_ == 'expenses' else False

            add_transaction(amount, type_, category, subcategory, description, date_str, optional)
            messagebox.showinfo("Успех", "Транзакция добавлена!")
            reset_form_fields()
            back_callback()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить транзакцию: {e}")

    def on_type_selected(event):
        update_categories()
        category_cb.config(state="readonly")

    center_wrapper = tk.Frame(frame)
    center_wrapper.pack(expand=True, anchor='n')  # сверху, с отступом

    form = tk.Frame(center_wrapper)
    form.pack()

    # Настраиваем форму, чтобы колонка расширялась
    form.columnconfigure(0, weight=1)

    # --- Рамка ---
    around_frame = tk.LabelFrame(form, text="Добавление транзакции", padx=10, pady=10, width=700, height=200)
    around_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    around_frame.grid_propagate(False)
    around_frame.columnconfigure(0, weight=1)  # Чтобы содержимое могло центрироваться

    # Обёртка для колонок
    # around_inner = tk.Frame(around_frame)
    # around_inner.place(relx=0.5, rely=0.5, anchor='center')  # <-- Центрирование по вертикали и горизонтали

    around_column_1 = tk.Frame(around_frame)
    around_column_1.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

    # Длина столбца
    label_width = 16

    # ======= Левая часть =======

    # ---Сумма ---
    vcmd = around_column_1.register(validate_amount_input)
    tk.Label(around_column_1, text="Сумма:",width=label_width,  anchor='w').grid(row=0, column=0, sticky='w', padx=0, pady=5)
    amount_entry = tk.Entry(around_column_1, textvariable=amount_var, validate='key', validatecommand=(vcmd, '%P'))
    amount_entry.grid(row=0, column=1, padx=10, pady=5)

    # --- Описание ---
    tk.Label(around_column_1, text="Описание:", width=label_width, anchor='w').grid(row=1, column=0, sticky='w', padx=0, pady=5)
    tk.Entry(around_column_1, textvariable=description_var).grid(row=1, column=1, padx=10, pady=5)

    # --- Дата ---
    tk.Label(around_column_1, text="Дата (ДД-ММ-ГГГГ):", width=label_width, anchor='w').grid(row=2, column=0, sticky='w', padx=0, pady=5)
    # Привязываем валидацию
    vcmd = (around_column_1.register(validate_date_input), "%P")
    date_entry = ttk.Entry(around_column_1, textvariable=date_var, validate="key", validatecommand=vcmd)
    date_entry.grid(row=2, column=1, padx=10, pady=5)

    # Привязываем автоформатирование после каждой клавиши
    date_entry.bind("<KeyRelease>", lambda e: auto_format_date_input(e, date_entry, date_var))
    
    # ======= Правая часть =======

    # --- Тип ---
    tk.Label(around_column_1, text="Тип:", width=label_width, anchor='w').grid(row=0, column=2, sticky='w', padx=0, pady=5)
    type_cb = ttk.Combobox(around_column_1, textvariable=type_var, state='readonly')
    type_cb['values'] = list(type_display.values())
    type_cb.grid(row=0, column=3, padx=0, pady=5)
    type_cb.bind('<<ComboboxSelected>>', on_type_selected)

    # --- Категория ---
    tk.Label(around_column_1, text="Категория:",width=label_width, anchor='w').grid(row=1, column=2, sticky='w', padx=0, pady=5)
    category_cb = ttk.Combobox(around_column_1, textvariable=category_var, state='disabled')
    category_cb.grid(row=1, column=3, padx=0, pady=0)
    category_cb.bind('<<ComboboxSelected>>', update_subcategories)

    # --- Подкатегория ---
    subcategory_label = tk.Label(around_column_1, text="Подкатегория:", width=label_width, anchor='w')
    subcategory_cb = ttk.Combobox(around_column_1, textvariable=subcategory_var, state='readonly')
    subcategory_cb.bind('<<ComboboxSelected>>', remove_combobox_selection(subcategory_cb))
    optional_cb = ttk.Checkbutton(around_column_1, text="Необязательный расход", variable=optional_var)

    # ======= Кнопки снизу =======
    buttons_frame = tk.Frame(frame)
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Сохранить", command=save_transaction).pack(side='left', padx=10)
    ttk.Button(buttons_frame, text="Назад", command=handle_back).pack(side='left', padx=10)
