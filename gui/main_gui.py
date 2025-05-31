import tkinter as tk
from tkinter import messagebox, ttk
import ctypes
from .add_transaction_ui import create_add_transaction_ui  
from .delete_transaction_ui import create_delete_transaction_ui
from .find_transaction_to_edit_ui import create_find_transaction_to_edit_ui
from .transactions_list_filter_ui import create_transaction_filter_window
from gui.cat_and_sub.move_transactions_ui import create_move_transaction_ui
from gui.cat_and_sub.cat_and_sub_list_ui import create_cat_and_sub_list
from gui.cat_and_sub.cat_and_sub_rename_ui import create_rename_ui
from gui.cat_and_sub.cat_and_sub_delete_ui import create_delete_ui
from gui.cat_and_sub.cat_and_sub_add_ui import create_add_ui
from category import load_categories
from .utils_gui import show_frame

def run_gui():

    categories_data = load_categories()

    # --- Включаем DPI-aware режим (важно для чётких шрифтов на Windows) ---
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Для Windows 8.1 и выше
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()  # Для Windows 7
        except Exception:
            pass

    # === Назад ===
    def back_to_main():
        root.title("Управление финансами")
        show_frame(main_menu, frame_data)

    def back_to_transactions():
        root.title("Управление финансами | Транзакции")
        show_frame(transactions_menu, frame_data)

    def back_to_cat_and_sub():
        root.title("Управление финансами | Категории и подкатегории")
        show_frame(cat_and_sub_menu, frame_data)

    def back_to_cat_and_sub_change():
        root.title("Управление финансами | Категории и подкатегории")
        show_frame(cat_and_sub_change_menu, frame_data)

    # --- Функция переключения экранов ---
    def go_to_edit_transaction():
        root.title("Управление финансами | Транзакции | Редактирование транзакции")
        show_frame(find_transaction_to_edit_frame, frame_data)

    def go_list_of_transactions():
        root.title("Управление финансами | Транзакции | Список транзакции")
        show_frame(list_of_transactions_frame, frame_data)

    # === Главное окно ===
    root = tk.Tk()
    root.title('Управление финансами')
    root.geometry("800x500")

    # === Фреймы ===
    main_menu = tk.Frame(root)

    # --- Фреймы управления транзакциями ---
    transactions_menu = tk.Frame(root)  
    add_transaction_frame = tk.Frame(root)
    delete_transaction_frame = tk.Frame(root)
    find_transaction_to_edit_frame = tk.Frame(root)
    edit_transaction_frame = tk.Frame(root)
    list_of_transactions_frame = tk.Frame(root)

    # --- Фреймы управления категориями ---
    cat_and_sub_menu = tk.Frame(root)
    cat_and_sub_list_frame = tk.Frame(root)
    move_transactions_frame = tk.Frame(root)
    cat_and_sub_change_menu = tk.Frame(root)
    cat_and_sub_rename_frame = tk.Frame(root)
    cat_and_sub_delete_frame = tk.Frame(root)
    cat_and_sub_add_frame = tk.Frame(root)

    frame_data = [main_menu, transactions_menu, add_transaction_frame,delete_transaction_frame, 
                  find_transaction_to_edit_frame, edit_transaction_frame, list_of_transactions_frame, cat_and_sub_menu,
                  cat_and_sub_list_frame, move_transactions_frame, cat_and_sub_change_menu, cat_and_sub_rename_frame,
                  cat_and_sub_delete_frame, cat_and_sub_add_frame]

    # --- Главное меню ---
    main_button_container = tk.Frame(main_menu)
    main_button_container.pack(expand=True)

    ttk.Button(main_button_container, text="Управление транзакциями", width=40, command=lambda: [root.title("Управление финансами | Транзакции"), show_frame(transactions_menu, frame_data)]).pack(pady=5)
    ttk.Button(main_button_container, text="Управление категориями", width=40, command=lambda: [root.title("Управление финансами | Категории и подкатегории"), show_frame(cat_and_sub_menu, frame_data)]).pack(pady=5)
    ttk.Button(main_button_container, text="Статистика", width=40, command=lambda: messagebox.showinfo('Статистика', 'Окно со статистикой')).pack(pady=5)
    ttk.Button(main_button_container, text="Отчёты", width=40, command=lambda: messagebox.showinfo('Отчёты', 'Окно с отчетами')).pack(pady=5)
    ttk.Button(main_button_container, text="Выход", width=40, command=root.quit).pack(pady=5)


    # --- Меню управления транзакциями ---
    transactions_button_container = tk.Frame(transactions_menu)
    transactions_button_container.pack(expand=True)

    ttk.Button(transactions_button_container, text="Добавить транзакцию", width=40, 
               command=lambda: [root.title("Управление финансами | Транзакции | Добавление транзакции"), 
                                create_add_transaction_ui(add_transaction_frame, categories_data, show_frame, frame_data, back_to_transactions)]).pack(pady=5)
    ttk.Button(transactions_button_container, text="Удалить транзакцию", width=40, 
               command=lambda: [root.title("Управление финансами | Транзакции | Удаление транзакции"), 
                                show_frame(delete_transaction_frame, frame_data)]).pack(pady=5)
    ttk.Button(transactions_button_container, text="Изменить транзакцию", width=40, command=go_to_edit_transaction).pack(pady=5)
    ttk.Button(transactions_button_container, text="Список транзакций", width=40, command=go_list_of_transactions).pack(pady=5)
    ttk.Button(transactions_button_container, text="Назад", command=back_to_main, width=40).pack(pady=5)


    # --- Меню управления категориями и подкатегориями ---
    cat_and_sub_button_container = tk.Frame(cat_and_sub_menu)
    cat_and_sub_button_container.pack(expand=True)

    ttk.Button(cat_and_sub_button_container, text="Изменение категории или подкатегории", width=40, 
               command=lambda: show_frame(cat_and_sub_change_menu, frame_data)).pack(pady=5)
    
    ttk.Button(cat_and_sub_button_container, text="Перевод между категориями", width=40, 
               command=lambda: [root.title("Управление финансами | Категории и подкатегории | Перевод транзакций"), 
                                 create_move_transaction_ui(move_transactions_frame, frame_data, back_to_cat_and_sub)]).pack(pady=5)
    
    ttk.Button(cat_and_sub_button_container, text="Список категорий и подкатегорий", width=40,
                command=lambda: [root.title("Управление финансами | Категории и подкатегории | Список"), 
                                 create_cat_and_sub_list(cat_and_sub_list_frame, frame_data, back_to_cat_and_sub)]).pack(pady=5)
    ttk.Button(cat_and_sub_button_container, text="Назад", command=back_to_main, width=40).pack(pady=5)


    # --- Меню изменения категорий\подкатегорий ---
    cat_and_sub_change_button_container = tk.Frame(cat_and_sub_change_menu)
    cat_and_sub_change_button_container.pack(expand=True)

    ttk.Button(cat_and_sub_change_button_container, text="Добавление", width=40,
                command=lambda: [root.title("Управление финансами | Категории и подкатегории | Добавление"),
                                create_add_ui(cat_and_sub_add_frame, frame_data, back_to_cat_and_sub_change)]).pack(pady=5)
    ttk.Button(cat_and_sub_change_button_container, text="Удаление", width=40, 
               command=lambda: [root.title("Управление финансами | Категории и подкатегории | Удаление"),
                                create_delete_ui(cat_and_sub_delete_frame, frame_data, back_to_cat_and_sub_change)]).pack(pady=5)
    ttk.Button(cat_and_sub_change_button_container, text="Переименование", width=40, 
               command=lambda: [root.title("Управление финансами | Категории и подкатегории | Переименование"),
                                create_rename_ui(cat_and_sub_rename_frame, frame_data, back_to_cat_and_sub_change)]).pack(pady=5)
    ttk.Button(cat_and_sub_change_button_container, text="Назад", command=back_to_cat_and_sub, width=40).pack(pady=5)

    # === Транзакции ===

    # --- Форма удаления транзакции ---
    create_delete_transaction_ui(delete_transaction_frame, back_to_transactions)

    # --- Форма редактирования транзакции ---
    create_find_transaction_to_edit_ui(find_transaction_to_edit_frame, edit_transaction_frame,frame_data, back_to_transactions)

    # --- Форма списка транзакций ---
    create_transaction_filter_window(list_of_transactions_frame, back_to_transactions)

    # --- Стилизация кнопок ttk ---
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    # --- Запуск интерфейса с главного меню ---
    show_frame(main_menu, frame_data)
    root.mainloop()