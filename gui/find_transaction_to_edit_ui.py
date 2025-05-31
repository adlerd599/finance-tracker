import tkinter as tk
from tkinter import ttk, messagebox
from .utils_gui import find_transaction_by_id, validate_id_input, show_frame
from .edit_transaction_ui import open_edit_form

def create_find_transaction_to_edit_ui(frame_search, frame_edit, data, back_callback):
    
    for widget in frame_search.winfo_children():
        widget.destroy()

    id_var = tk.StringVar()
    
    def handle_search():
        transaction_id = id_var.get()
        item = find_transaction_by_id(transaction_id)

        if item:
            messagebox.showinfo("Найдено", f"Найдена транзакция с ID: {transaction_id} !")
            id_var.set("")
            show_frame(frame_edit, data)
            open_edit_form(frame_edit, item, back_callback)
    
    def handle_back():
        id_var.set("")
        back_callback()

    # --- Форма ---
    # tk.Label(frame_search, text="Редактирование транзакции:", font=("Helvetica", 12)).pack(pady=10)

    center_wrapper = tk.Frame(frame_search)
    center_wrapper.pack(expand=True, anchor='n')  # сверху, с отступом

    form = tk.Frame(center_wrapper)
    form.pack()

    # --- Рамка ---
    around_frame = tk.LabelFrame(form, text="Редактирование транзакции | Поиск по ID", padx=10, pady=10, width=700, height=200)
    around_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    around_frame.grid_propagate(False)
    around_frame.columnconfigure(0, weight=1)  # Чтобы содержимое могло центрироваться

    # Обёртка для колонок
    around_inner = tk.Frame(around_frame)
    around_inner.place(relx=0.5, rely=0.5, anchor='center')  # <-- Центрирование по вертикали и горизонтали

     # --- Поле ввода ID ---
    tk.Label(around_inner, text="ID транзакции (6 цифр):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    vcmd = frame_search.register(validate_id_input)
    id_entry = tk.Entry(around_inner, textvariable=id_var, validate='key', validatecommand=(vcmd, '%P'))
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    # --- Кнопки ---
    buttons_frame = tk.Frame(frame_search)
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Поиск", command=handle_search).pack(side="left", padx=10)
    ttk.Button(buttons_frame, text="Назад", command=handle_back).pack(side="left", padx=10)