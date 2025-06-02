import tkinter as tk
from tkinter import ttk, messagebox
from app.transaction import delete_transaction
from gui.utils_gui import find_transaction_by_id, validate_id_input

def create_delete_transaction_ui(frame, back_callback):
    id_var = tk.StringVar()

    def handle_delete():
        transaction_id = id_var.get()
        item = find_transaction_by_id(transaction_id)

        if item:
                # Найдена: показываем инфо и спрашиваем подтверждение
                type_name = "Доходы" if item["type_"] == "income" else "Расходы"
                summary = (
                    f"ID: {transaction_id}\n"
                    f"Тип: {type_name}\n"
                    f"Категория: {item['category']}\n"
                    f"Сумма: {item['amount']}\n"
                    f"Дата: {item['date']}"
                )
        
                # Подтверждение перед удалением
                confirm = messagebox.askyesno("Подтверждение", f"Удалить эту транзакцию?\n\n{summary}")
                if not confirm:
                    return  # Пользователь отменил
                
                result = delete_transaction(transaction_id)
                if result["success"]:
                    messagebox.showinfo("Успех", result["message"])
                    id_var.set("")
                    back_callback()
                else:
                    messagebox.showerror("Ошибка", result["message"])
                return

    def handle_back():
        id_var.set("")
        back_callback()

    # --- Форма ---

    center_wrapper = tk.Frame(frame)
    center_wrapper.pack(expand=True, anchor='n')  # сверху, с отступом

    form = tk.Frame(center_wrapper)
    form.pack()

    # --- Рамка ---
    around_frame = tk.LabelFrame(form, text="Удаление транзакции | Поиск по ID", padx=10, pady=10, width=700, height=200)
    around_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    around_frame.grid_propagate(False)
    around_frame.columnconfigure(0, weight=1)  # Чтобы содержимое могло центрироваться

    # Обёртка для колонок
    around_inner = tk.Frame(around_frame)
    around_inner.place(relx=0.5, rely=0.5, anchor='center')  # <-- Центрирование по вертикали и горизонтали

     # --- Поле ввода ID ---
    tk.Label(around_inner, text="ID транзакции (6 цифр):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    vcmd = frame.register(validate_id_input) 
    id_entry = tk.Entry(around_inner, textvariable=id_var, validate='key', validatecommand=(vcmd, '%P'))
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    # --- Кнопки ---
    buttons_frame = tk.Frame(frame)
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Удалить", command=handle_delete).pack(side="left", padx=10)
    ttk.Button(buttons_frame, text="Назад", command=handle_back).pack(side="left", padx=10)