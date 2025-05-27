import tkinter as tk
from tkinter import messagebox, ttk
import ctypes
from transaction import load_data
from gui.add_transaction_ui import create_add_transaction_ui  # импортируем UI добавления транзакции
from gui.delete_transaction_ui import create_delete_transaction_ui
from category import load_categories

def run_gui():
    # --- Включаем DPI-aware режим (важно для чётких шрифтов на Windows) ---
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Для Windows 8.1 и выше
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()  # Для Windows 7
        except Exception:
            pass

    def open_transactions():
        root.title("Управление финансами | Транзакции")
        show_frame(transactions_menu)

    # --- Назад ---
    def back_to_main():
        root.title("Управление финансами")
        show_frame(main_menu)

    def back_to_transactions():
        root.title("Управление финансами | Транзакции")
        show_frame(transactions_menu)

    # --- Функция переключения экранов ---
    def show_frame(frame):
        # Скрывает все фреймы
        for f in (main_menu, transactions_menu, add_transaction_frame,delete_transaction_frame):
            f.pack_forget()
        # Показывает нужный
        frame.pack(fill='both', expand=True)

    categories_data = load_categories()

    # --- Главное окно ---
    root = tk.Tk()
    root.title('Управление финансами')
    root.geometry("700x400")

    # --- Фреймы ---
    main_menu = tk.Frame(root)
    transactions_menu = tk.Frame(root)
    add_transaction_frame = tk.Frame(root)
    delete_transaction_frame = tk.Frame(root)

    # --- Главное меню ---
    main_button_container = tk.Frame(main_menu)
    main_button_container.pack(expand=True)

    ttk.Button(main_button_container, text="Управление транзакциями", width=40, command=open_transactions).pack(pady=5)
    ttk.Button(main_button_container, text="Управление категориями", width=40, command=lambda: messagebox.showinfo('Категории', 'Окно управления категориями')).pack(pady=5)
    ttk.Button(main_button_container, text="Статистика", width=40, command=lambda: messagebox.showinfo('Статистика', 'Окно со статистикой')).pack(pady=5)
    ttk.Button(main_button_container, text="Отчёты", width=40, command=lambda: messagebox.showinfo('Отчёты', 'Окно с отчетами')).pack(pady=5)
    ttk.Button(main_button_container, text="Выход", width=40, command=root.quit).pack(pady=5)

    # --- Меню управления транзакциями ---
    transactions_button_container = tk.Frame(transactions_menu)
    transactions_button_container.pack(expand=True)

    ttk.Button(transactions_button_container, text="Добавить транзакцию", width=40, command=lambda: [root.title("Управление финансами | Транзакции | Добавление транзакции"), show_frame(add_transaction_frame)]).pack(pady=5)
    ttk.Button(transactions_button_container, text="Удалить транзакцию", width=40, command=lambda: [root.title("Управление финансами | Транзакции | Удаление транзакции"), show_frame(delete_transaction_frame)]).pack(pady=5)
    ttk.Button(transactions_button_container, text="Изменить транзакцию", width=40).pack(pady=5)
    ttk.Button(transactions_button_container, text="Показать транзакции за период", width=40).pack(pady=5)
    ttk.Button(transactions_button_container, text="Назад", command=back_to_main, width=40).pack(pady=5)

    # --- Форма добавления транзакции ---
    create_add_transaction_ui(add_transaction_frame, categories_data, show_frame, back_to_transactions)

    # --- Форма удаления транзакции ---
    create_delete_transaction_ui(delete_transaction_frame, back_to_transactions)

    # --- Стилизация кнопок ttk ---
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    # --- Запуск интерфейса с главного меню ---
    show_frame(main_menu)
    root.mainloop()