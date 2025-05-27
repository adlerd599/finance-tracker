import tkinter as tk
from tkinter import ttk, messagebox
from transaction import add_transaction
from category import load_categories
from utils import validate_date

type_display = {
    'income': 'Доходы',
    'expenses': 'Расходы'
}

# Обратное соответствие:
type_reverse = {v: k for k, v in type_display.items()}

def create_add_transaction_ui(frame, categories_data, show_frame_callback, back_callback):
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

    # Появление подкатегорий
    def toggle_expense_fields():
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')

        if type_ == 'expenses':
            subcategory_label.grid(row=2, column=2, sticky='w', padx=0, pady=5)
            subcategory_cb.grid(row=2, column=3, padx= 0, pady=5)
            optional_cb.grid(row=3, column=2, columnspan=3, sticky='w', padx= 0, pady=5)
        else:
            subcategory_label.grid_forget()
            subcategory_cb.grid_forget()
            optional_cb.grid_forget()

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
        if date_str.strip():
            validated_date = validate_date(date_str)
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
            date_str = date_var.get()
            optional = optional_var.get() if type_ == 'expenses' else False

            add_transaction(amount, type_, category, subcategory, description, date_str, optional)
            messagebox.showinfo("Успех", "Транзакция добавлена!")
            reset_form_fields()
            back_callback()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить транзакцию: {e}")

    # Не пропускает не цифры
    def validate_amount_input(new_value):
        if new_value == "":
            return True  # позволить очистку поля
        try:
            float(new_value)
            return True
        except ValueError:
            return False
        
    def format_date_input(event):
        value = date_var.get().replace("-", "")
        
        # Ограничиваем только цифрами и максимум 8 символов
        if not value.isdigit():
            value = ''.join(filter(str.isdigit, value))
        value = value[:8]

        # Добавляем тире после 2 и 4 цифр
        formatted = ""
        if len(value) >= 2:
            formatted += value[:2]
            if len(value) >= 4:
                formatted += "-" + value[2:4]
                if len(value) > 4:
                    formatted += "-" + value[4:]
                else:
                    formatted += "-"
            else:
                formatted += "-"
                formatted += value[2:]
        else:
            formatted = value

        # Обновляем поле
        date_var.set(formatted)
    
    # Длина столбца
    label_width = 16

    # Внешний контейнер для центрирования по горизонтали
    tk.Label(frame, text="Добавление транзакции:", font=("Arial", 14)).pack(pady=10)

    center_wrapper = tk.Frame(frame)
    center_wrapper.pack(expand=True, anchor='n', pady=30)  # сверху, с отступом

    form = tk.Frame(center_wrapper)
    form.pack()

    # ======= Левая часть =======

    # ---Сумма ---
    vcmd = form.register(validate_amount_input)
    tk.Label(form, text="Сумма:", width=label_width, anchor='w').grid(row=0, column=0, sticky='w', padx=0, pady=5)
    amount_entry = tk.Entry(form, textvariable=amount_var, validate='key', validatecommand=(vcmd, '%P'))
    amount_entry.grid(row=0, column=1, padx=10, pady=5)

    # --- Описание ---
    tk.Label(form, text="Описание:", width=label_width, anchor='w').grid(row=1, column=0, sticky='w', padx=0, pady=5)
    tk.Entry(form, textvariable=description_var).grid(row=1, column=1, padx=10, pady=5)

    # --- Дата ---
    tk.Label(form, text="Дата (ДД-ММ-ГГГГ):", width=label_width, anchor='w').grid(row=2, column=0, sticky='w', padx=0, pady=5)
    # Поле ввода даты
    date_entry = tk.Entry(form, textvariable=date_var)
    date_entry.grid(row=2, column=1, padx=10, pady=5)
    date_entry.bind('<KeyRelease>', format_date_input)
    
    # ======= Правая часть =======

    # --- Тип ---
    tk.Label(form, text="Тип:", width=label_width, anchor='w').grid(row=0, column=2, sticky='w', padx=0, pady=5)
    type_cb = ttk.Combobox(form, textvariable=type_var, state='readonly')
    type_cb['values'] = list(type_display.values())
    type_cb.grid(row=0, column=3, padx=0, pady=5)
    type_cb.bind('<<ComboboxSelected>>', update_categories)

    # --- Категория ---
    tk.Label(form, text="Категория:", width=label_width, anchor='w').grid(row=1, column=2, sticky='w', padx=0, pady=5)
    category_cb = ttk.Combobox(form, textvariable=category_var, state='readonly')
    category_cb.grid(row=1, column=3, padx=0, pady=0)
    category_cb.bind('<<ComboboxSelected>>', update_subcategories)

    # --- Подкатегория ---
    subcategory_label = tk.Label(form, text="Подкатегория:", width=label_width, anchor='w')
    subcategory_cb = ttk.Combobox(form, textvariable=subcategory_var, state='readonly')
    optional_cb = ttk.Checkbutton(form, text="Необязательный расход", variable=optional_var)

    # ======= Кнопки снизу =======
    buttons_frame = tk.Frame(frame)
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Сохранить", command=save_transaction).pack(side='left', padx=10)
    ttk.Button(buttons_frame, text="Назад", command=handle_back).pack(side='left', padx=10)
