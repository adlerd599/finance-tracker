import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.analysis import filter_transactions_by_period
from app.utils import validate_date
from app.transaction import load_data  
from .transactions_list_view_ui import show_filtered_transactions
from .utils_gui import validate_date_input, auto_format_date_input, remove_combobox_selection

def create_transaction_filter_window(frame, back_callback):
    for widget in frame.winfo_children():
        widget.destroy()

    # Переменные
    filter_mode = tk.StringVar(value="last")  # 'last' или 'date'
    last_n_var = tk.StringVar(value="10")
    date_from_var = tk.StringVar()
    date_to_var = tk.StringVar()

    def reset_fields():
        filter_mode.set("last")
        last_n_var.set("10")
        date_from_var.set("")
        date_to_var.set("")
        toggle_filter_inputs()

    # Обработка переключения фильтра
    def toggle_filter_inputs():
        if filter_mode.get() == "last":
            last_n_cb.config(state='readonly')
            date_from_entry.config(state='disabled')
            date_to_entry.config(state='disabled')
        else:
            last_n_cb.config(state='disabled')
            date_from_entry.config(state='normal')
            date_to_entry.config(state='normal')

    # Кнопка запуска фильтрации
    def apply_filter():
        transactions = load_data()

        if filter_mode.get() == "last":
            try:
                n = int(last_n_var.get())
                result = transactions[-n:][::-1]
                sort_by = f"по последним {n} добавленным"
                show_filtered_transactions(result, sort_by)
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное количество транзакций.")
        else:
            date_from = date_from_var.get()
            date_to = date_to_var.get()

            validated_from = validate_date(date_from)
            validated_to = validate_date(date_to)

            if not validated_from or not validated_to:
                messagebox.showerror("Ошибка", "Введите даты в формате ДД-ММ-ГГГГ.")
                return
            
            # Сравнение дат
            from_dt = datetime.strptime(validated_from, "%d-%m-%Y")
            to_dt = datetime.strptime(validated_to, "%d-%m-%Y")

            if from_dt > to_dt:
                messagebox.showerror("Ошибка", "Дата 'от' не может быть позже даты 'до'.")
                return

            result = filter_transactions_by_period(transactions, date_from, date_to)
            if result is None:
                messagebox.showerror("Ошибка", "Ошибка при фильтрации по датам.")
                return
            
            if result:
                sort_by = f"от {validated_from} до {validated_to}"
                show_filtered_transactions(result, sort_by)
            else :
                messagebox.showerror("Ошибка", "Транзакции не найдены.")

    # Внешний контейнер для центрирования по горизонтали
    center_wrapper = tk.Frame(frame)
    center_wrapper.pack(expand=True, anchor='n')  # сверху, с отступом

    form = tk.Frame(center_wrapper)
    form.pack()

    # Настраиваем форму, чтобы колонка расширялась
    form.columnconfigure(0, weight=1)

    # --- Рамка ---
    filter_frame = tk.LabelFrame(form, text="Фильтрация транзакций", padx=10, pady=10, width=700, height=350)
    filter_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    filter_frame.grid_propagate(False)
    filter_frame.columnconfigure(0, weight=1)  # Чтобы содержимое могло центрироваться

    # Обёртка для колонок
    filter_inner = tk.Frame(filter_frame)
    filter_inner.place(relx=0.5, rely=0.5, anchor='center')  # <-- Центрирование по вертикали и горизонтали

    # Вложенный фрейм для полей даты
    date_frame = tk.Frame(filter_inner)
    date_frame.grid(row=1, column=0, sticky="w", padx=50, pady=5)
    vcmd = (date_frame.register(validate_date_input), "%P")

    # --- Радио-кнопка "По дате" ---
    tk.Radiobutton(filter_inner, text="Фильтр по дате:", variable=filter_mode, value="date",
                   command=toggle_filter_inputs).grid(row=0, column=0, sticky="w", padx=5, pady=5)

    tk.Label(date_frame, text="от:").grid(row=1, column=0, sticky='e', padx=10)
    date_from_entry = ttk.Entry(date_frame, textvariable=date_from_var, validate="key", validatecommand=vcmd, state='disabled', width=12)
    date_from_entry.grid(row=1, column=1, padx=0)

    tk.Label(date_frame, text="до:").grid(row=1, column=2, sticky='e', padx=10)
    date_to_entry = ttk.Entry(date_frame, textvariable=date_to_var, validate="key", validatecommand=vcmd, state='disabled', width=12)
    date_to_entry.grid(row=1, column=3, padx=0) 

    # Привязываем автоформатирование после каждой клавиши
    date_from_entry.bind("<KeyRelease>", lambda e: auto_format_date_input(e, date_from_entry, date_from_var))
    date_to_entry.bind("<KeyRelease>", lambda e: auto_format_date_input(e, date_to_entry, date_to_var))


    # --- Радио-кнопка "Последние N транзакций" ---
    tk.Radiobutton(filter_inner, text="Последние добавленные транзакции:", variable=filter_mode, value="last",
                   command=toggle_filter_inputs).grid(row=2, column=0, sticky="w", padx=5, pady=(50,0))

    last_frame = tk.Frame(filter_inner)
    last_frame.grid(row=3, column=0, sticky="w", padx=50, pady=5)

    tk.Label(last_frame, text="Показать всего:").grid(row=3, column=0, sticky='e', padx=10)
    last_n_cb = ttk.Combobox(last_frame, textvariable=last_n_var, state='readonly', width=10)
    last_n_cb['values'] = [5, 10, 20, 50, 100]
    last_n_cb.grid(row=3, column=1, padx=5, pady=5)

    last_n_cb.bind("<<ComboboxSelected>>", remove_combobox_selection(last_n_cb))

    # --- Кнопки ---
    buttons_frame = tk.Frame(frame)
    buttons_frame.pack(pady=20)

    # Кнопка "Показать"
    ttk.Button(buttons_frame, text="Показать", command=apply_filter).pack(side="left", padx=10)

    # Кнопка "Назад"
    ttk.Button(buttons_frame, text="Назад", command=lambda: (reset_fields(),back_callback())).pack(side="left", padx=10)

    toggle_filter_inputs()  # начальная инициализация