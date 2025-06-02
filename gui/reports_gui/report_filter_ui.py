import tkinter as tk
from tkinter import ttk, messagebox
from app.transaction import load_data
from app.analysis import filter_transactions_by_period
from gui.utils_gui import show_frame
from gui.utils_gui import validate_date_input, auto_format_date_input
from gui.reports_gui.report_view_ui import show_report
from app.analysis import (
    total_income,
    total_expenses,
    total_balace,
    sum_income_by_categories,
    sum_expenses_by_categories,
    sum_by_sub_for_expenses,
    count_optional_expenses
)

def create_report_filter_window(frame, data, back_callback):

    for widget in frame.winfo_children():
        widget.destroy()

    show_frame(frame, data)

    report_name_var = tk.StringVar()
    date_from_var = tk.StringVar()
    date_to_var = tk.StringVar()

    def handle_generate_report():

        all_data = load_data()
        report_name = report_name_var.get().strip()
        date_from = date_from_var.get()
        date_to = date_to_var.get()

        result = filter_transactions_by_period(all_data, date_from, date_to)

        if result['success']:
            filtered = result['transactions']

             # Строим словарь с данными отчета
            report_data = {
                "report_name": report_name if report_name else None,
                "date_from": date_from,
                "date_to": date_to,
                "summary": {
                    "income": total_income(filtered),
                    "expenses": total_expenses(filtered),
                    "balance": total_balace(filtered),
                },
                "categories": {
                    "income": sum_income_by_categories(filtered),
                    "expenses": sum_expenses_by_categories(filtered),
                    "expenses_by_sub": sum_by_sub_for_expenses(filtered),
                },
                "optional_expenses": {
                    "total": count_optional_expenses(filtered)[0],
                    "optional": count_optional_expenses(filtered)[1],
                },
                "transactions": filtered
            }

            show_report(report_data)

            report_name_var.set('')
            date_from_var.set('')
            date_to_var.set('')

        else:
            messagebox.showerror("Ошибка", result["message"])

    # --- Центрирующая обёртка ---
    center_wrapper = tk.Frame(frame)
    center_wrapper.pack(expand=True, anchor='n')

    form = tk.Frame(center_wrapper)
    form.pack()

    form.columnconfigure(0, weight=1)

    # --- Рамка фильтров ---
    filter_frame = tk.LabelFrame(form, text="Генерация отчёта", padx=20, pady=20, width=700, height=350)
    filter_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
    filter_frame.grid_propagate(False)
    filter_frame.columnconfigure(0, weight=1)

    # --- Центрированная обёртка ---
    filter_inner = tk.Frame(filter_frame)
    filter_inner.place(relx=0.5, rely=0.5, anchor="center")

    # --- Название отчета ---
    name_frame = tk.Frame(filter_inner)
    name_frame.grid(row=0, column=0, pady=10, sticky='w')

    tk.Label(name_frame, text="Название отчёта (необязательно):").grid(row=0, column=0, sticky="w", padx=(0, 10))
    tk.Entry(name_frame, textvariable=report_name_var, width=40).grid(row=1, column=0, pady=5)

    # --- Период отчётности ---
    date_frame = tk.Frame(filter_inner)
    date_frame.grid(row=1, column=0, pady=10, sticky='w')
    date_frame.columnconfigure((0, 2), weight=0)
    date_frame.columnconfigure((1, 3), weight=1, uniform='date')

    vcmd = (date_frame.register(validate_date_input), "%P")

    tk.Label(date_frame, text="Период отчётности:").grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 5))

    tk.Label(date_frame, text="от:").grid(row=1, column=0, sticky='e', padx=(0, 5))
    date_from_entry = tk.Entry(date_frame, textvariable=date_from_var, validate="key", validatecommand=vcmd, width=15)
    date_from_entry.grid(row=1, column=1, padx=(0, 10))

    tk.Label(date_frame, text="до:").grid(row=1, column=2, sticky='e', padx=(0, 5))
    date_to_entry = tk.Entry(date_frame, textvariable=date_to_var, validate="key", validatecommand=vcmd, width=15)
    date_to_entry.grid(row=1, column=3)

    # Автоформат даты
    date_from_entry.bind("<KeyRelease>", lambda e: auto_format_date_input(e, date_from_entry, date_from_var))
    date_to_entry.bind("<KeyRelease>", lambda e: auto_format_date_input(e, date_to_entry, date_to_var))

    # --- Кнопки внизу ---
    buttons_frame = tk.Frame(frame)
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Создать", command=handle_generate_report).pack(side="left", padx=10)
    ttk.Button(buttons_frame, text="Назад", command=back_callback).pack(side="left", padx=10)
