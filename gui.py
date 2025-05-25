import tkinter as tk
from tkinter import messagebox, ttk
import ctypes

# --- Включаем DPI-aware режим (важно для чётких шрифтов на Windows) ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Для Windows 8.1 и выше
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()  # Для Windows 7
    except Exception:
        pass


# Функции заглушки
def open_transactions():
    messagebox.showinfo('Транзакции', 'Окно управления транзакциями')

def open_categories():
    messagebox.showinfo('Категории', 'Окно управления категориями')

def open_statistics():
    messagebox.showinfo('Статистика', 'Окно со статистикой')

def open_reports():
    messagebox.showinfo('Отчёты', 'Окно с отчетами')

# --- Главное меню ---
root = tk.Tk()
root.title('Управление финансами')
root.geometry("700x400")

# --- Стилизация кнопок ttk ---
style = ttk.Style()
style.theme_use('default')

# Настраиваем стиль для кнопок
style.configure("TButton", font=("Helvetica", 12), padding=10)

# --- Контейнер для кнопок ---
frame = tk.Frame(root)
frame.pack(expand=True) # Центрирует по вертикали и горизонтали

# --- Заголоволок ---
#title = tk.Label(frame, text="Главное меню:", font=('Arial', 18))
#title.pack(pady=10)


btn_transactions = ttk.Button(frame, text="Управление транзакциями", width=40, command=open_transactions)
btn_categories = ttk.Button(frame, text="Управление категориями", width=40, command=open_categories)
btn_statistics = ttk.Button(frame, text="Статистика", width=40, command=open_statistics)
btn_reports = ttk.Button(frame, text="Отчёты", width=40, command=open_reports)

btn_transactions.pack(pady=5)
btn_categories.pack(pady=5)
btn_statistics.pack(pady=5)
btn_reports.pack(pady=5)

# --- Запуск интерфейса ---
root.mainloop()