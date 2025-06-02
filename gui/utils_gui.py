import tkinter as tk
from tkinter import messagebox
from app.transaction import load_data

# Поиск транзакции по ID
def find_transaction_by_id(transaction_id):

    # Длина ID должна быть - 6 цифр.
    if len(transaction_id) != 6:
            messagebox.showerror("Ошибка", "ID должен содержать ровно 6 цифр.")
            return None
        
    data = load_data()
    for item in data:
        if str(item.get("id")) == transaction_id:
            return item
        
    messagebox.showerror("Ошибка", f"Транзакция ID {transaction_id} не найдена.")
    return None

# Валидирует ввод ID: только цифры, не более 6 символов.
def validate_id_input(new_value):
        if new_value == "":
            return True  # разрешаем очистку
        return new_value.isdigit() and len(new_value) <= 6

# Валидирует ввод Суммы: только цифры, тип данных: float.
def validate_amount_input(new_value):
    if new_value == "":
        return True  # позволить очистку поля
    try:
        float(new_value)
        return True
    except ValueError:
        return False

# Валидирует ввод Даты: Разрешаем только цифры и тире, длина не более 10 символов    
def validate_date_input(new_value):
    if new_value == "":
        return True
    return all(c.isdigit() or c == '-' for c in new_value) and len(new_value) <= 10

# Валидирует ввод Даты: Автоматическое добавление тире "-"
def auto_format_date_input(event, entry_widget, date_var):
    if event.keysym in ("BackSpace", "Delete"):
        return  # не мешаем удалению

    value = date_var.get()
    cursor_pos = entry_widget.index(tk.INSERT)

    # Удаляем все тире
    digits_only = value.replace("-", "")

    if not digits_only.isdigit():
        return

    digits_only = digits_only[:8]

    formatted = ""
    for i, char in enumerate(digits_only):
        if i == 2 or i == 4:
            formatted += "-"
            if cursor_pos > i:
                cursor_pos += 1  # сдвигаем курсор из-за вставки "-"
        formatted += char

    date_var.set(formatted)

    # Устанавливаем откорректированную позицию курсора
    entry_widget.icursor(min(cursor_pos, len(formatted)))

# Фреймы
def show_frame(frame, data):
    # Скрывает все фреймы
    for f in data:
        f.pack_forget()
    # Показывает нужный
    frame.pack(fill='both', expand=True)

# Снимает выделение текста и устанавливает курсор в конец для ttk.Combobox.
# Удобно вызывать в обработчике события <<ComboboxSelected>>.
def remove_combobox_selection(combobox):
    def on_select(event=None):
        combobox.selection_clear()
        combobox.icursor(tk.END)
    return on_select