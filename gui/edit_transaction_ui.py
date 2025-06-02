import tkinter as tk
from tkinter import ttk, messagebox
from app.transaction import update_transaction_by_id
from app.category import load_categories
from app.utils import validate_date
from .utils_gui import validate_amount_input, validate_date_input, auto_format_date_input, remove_combobox_selection

type_display = {
    'income': 'Доходы',
    'expenses': 'Расходы'
}

# Обратное соответствие:
type_reverse = {v: k for k, v in type_display.items()}

def open_edit_form(frame, transaction, back_callback):

    for widget in frame.winfo_children():
        widget.destroy()

    updated_fields = {}

    def handle_back():
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')

        if amount_var.get() != str(transaction['amount']):
            updated_fields['amount'] = amount_var.get()
        if type_ != transaction['type_']:
            updated_fields['type_'] = type_
        if category_var.get() != transaction['category']:
            updated_fields['category'] = category_var.get()
        if subcategory_var.get() != transaction.get('subcategory', ''):
            updated_fields['subcategory'] = subcategory_var.get()
        if description_var.get() != transaction.get('description', ''):
            updated_fields['description'] = description_var.get()
        if date_var.get() != transaction['date']:
            updated_fields['date'] = date_var.get()
        if optional_var.get() != transaction.get('optional', False):
            updated_fields['optional'] = optional_var.get()

        if updated_fields:
            confirm = messagebox.askyesno(
            "Подтверждение",
            "Вы уверены, что хотите выйти?\nНесохранённые изменения будут потеряны."
            )
            if not confirm:
                return
        
        back_callback()

    # --- Переменные ---
    amount_var = tk.StringVar(value=str(transaction['amount']))
    type_var = tk.StringVar(value=type_display[transaction['type_']])
    category_var = tk.StringVar(value=transaction['category'])
    subcategory_var = tk.StringVar(value=transaction.get('subcategory', ''))
    description_var = tk.StringVar(value=transaction.get('description', ''))
    date_var = tk.StringVar(value=transaction['date'])
    optional_var = tk.BooleanVar(value=transaction.get('optional', False))

    categories_data = load_categories()

    def update_categories(*args):
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
        subcategories = categories_data.get(type_, {}).get(category, [])

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
        
    def handle_save():
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')

        # Проверка даты
        date_str = date_var.get()
        if date_str != transaction['date']:
            validated_date = validate_date(date_str)
            if not validated_date:
                messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
                return

        if amount_var.get() != str(transaction['amount']):
            updated_fields['amount'] = amount_var.get()
        if type_ != transaction['type_']:
            updated_fields['type_'] = type_
        if category_var.get() != transaction['category']:
            updated_fields['category'] = category_var.get()
        if subcategory_var.get() != transaction.get('subcategory', ''):
            updated_fields['subcategory'] = subcategory_var.get()
        if description_var.get() != transaction.get('description', ''):
            updated_fields['description'] = description_var.get()
        if date_var.get() != transaction['date']:
            updated_fields['date'] = date_var.get()
        if optional_var.get() != transaction.get('optional', False):
            updated_fields['optional'] = optional_var.get()

        if not category_var.get():
            messagebox.showerror("Ошибка", "Пожалуйста, выберите категорию.")
            return

        if type_ == 'expenses':
            subcategories = categories_data.get(type_, {}).get(category_var.get(), [])
            if subcategories and not subcategory_var.get():
                messagebox.showerror("Ошибка", "Пожалуйста, выберите подкатегорию.")
                return

        if not updated_fields:
            messagebox.showinfo("Информация", "Изменений не обнаружено.")
            return

        result = update_transaction_by_id(transaction['id'], updated_fields)
        if result['success']:
            messagebox.showinfo("Успех", result['message'])
            back_callback()
            return
        else:
            messagebox.showerror("Ошибка", result['message'])
            return
    
     # Внешний контейнер для центрирования по горизонтали
    # tk.Label(frame, text="Редактирование транзакции:", font=("Helvetica", 12)).pack(pady=10)

    center_wrapper = tk.Frame(frame)
    center_wrapper.pack(expand=True, anchor='n')  # сверху, с отступом

    form = tk.Frame(center_wrapper)
    form.pack()

    # Настраиваем форму, чтобы колонка расширялась
    form.columnconfigure(0, weight=1)

    # --- Рамка ---
    around_frame = tk.LabelFrame(form, text="Редактирование транзакции", padx=10, pady=10, width=700, height=200)
    around_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    around_frame.grid_propagate(False)

    around_column_1 = tk.Frame(around_frame)
    around_column_1.grid(row=0, column=0, sticky='ew', padx=10, pady=5)


    # Длина столбца
    label_width = 16

    # ======= Левая часть =======

    # ---Сумма ---
    vcmd = around_column_1.register(validate_amount_input)
    tk.Label(around_column_1, text="Сумма:", width=label_width, anchor='w').grid(row=0, column=0, sticky='w', padx=0, pady=5)
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
    type_cb.bind('<<ComboboxSelected>>', update_categories)

    # --- Категория ---
    tk.Label(around_column_1, text="Категория:", width=label_width, anchor='w').grid(row=1, column=2, sticky='w', padx=0, pady=5)
    category_cb = ttk.Combobox(around_column_1, textvariable=category_var, state='readonly')
    category_cb.grid(row=1, column=3, padx=0, pady=0)
    category_cb.bind('<<ComboboxSelected>>', update_subcategories)

    # --- Подкатегория ---
    subcategory_label = tk.Label(around_column_1, text="Подкатегория:", width=label_width, anchor='w')
    subcategory_cb = ttk.Combobox(around_column_1, textvariable=subcategory_var, state='readonly')
    subcategory_cb.bind('<<ComboboxSelected>>', remove_combobox_selection(subcategory_cb))
    optional_cb = ttk.Checkbutton(around_column_1, text="Необязательный расход", variable=optional_var)

    # --- Восстановление логики интерфейса ---
    update_categories()
    category_var.set(transaction['category'])

    update_subcategories()
    subcategory_var.set(transaction.get('subcategory', ''))

    toggle_expense_fields()

    # ======= Кнопки снизу =======
    buttons_frame = tk.Frame(frame)
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Сохранить", command=handle_save).pack(side='left', padx=10)
    ttk.Button(buttons_frame, text="Назад", command=handle_back).pack(side='left', padx=10)
