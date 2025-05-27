import tkinter as tk
from tkinter import ttk, messagebox
from transaction import delete_transaction, load_data

def create_delete_transaction_ui(frame, back_callback):
    id_var = tk.StringVar()

    def validate_id_input(new_value):
        if new_value == "":
            return True  # разрешаем очистку
        return new_value.isdigit() and len(new_value) <= 6

    def handle_delete():
        transaction_id = id_var.get()
        
        if len(transaction_id) != 6:
            messagebox.showerror("Ошибка", "ID должен содержать ровно 6 цифр.")
            return
        
        data = load_data()
        for item in data:
            if str(item.get("id")) == transaction_id:
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
                else:
                    messagebox.showerror("Ошибка", result["message"])
                return

        # Если не найдено
        messagebox.showerror("Ошибка", f"Транзакция ID {transaction_id} не найдена.")

    def handle_back():
        id_var.set("")
        back_callback()

    # --- Форма ---
    tk.Label(frame, text="Удаление транзакции по ID:", font=("Arial", 14)).pack(pady=10)

    center_wrapper = tk.Frame(frame)
    center_wrapper.pack(expand=True, anchor='n', pady=30)  # сверху, с отступом

    form = tk.Frame(center_wrapper)
    form.pack()

     # --- Поле ввода ID ---
    tk.Label(form, text="ID транзакции (6 цифр):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    vcmd = frame.register(validate_id_input)  # <-- исправлено здесь
    id_entry = tk.Entry(form, textvariable=id_var, validate='key', validatecommand=(vcmd, '%P'))
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    # --- Кнопки ---
    buttons_frame = tk.Frame(frame)
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Удалить", command=handle_delete).pack(side="left", padx=10)
    ttk.Button(buttons_frame, text="Назад", command=handle_back).pack(side="left", padx=10)