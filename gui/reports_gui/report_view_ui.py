import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style as mpl_style
mpl_style.use("seaborn-v0_8-muted")  # стиль графиков

def show_report(report_data):
    window = tk.Toplevel()
    window.title("Список транзакций")
    window.geometry("1000x800")

    # --- Установка белой темы для виджетов ---
    style = ttk.Style(window)
    style.theme_use("default")
    style.configure("White.TFrame", background="white")
    style.configure("White.TLabelframe", background="white")
    style.configure("White.TLabelframe.Label", background="white")
    style.configure("White.TLabel", background="white")
    style.configure("TButton", padding=6, font=("Arial", 10))

    canvas = tk.Canvas(window, background="white")
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Фрейм внутри Canvas
    scroll_frame = ttk.Frame(canvas, style="White.TFrame")

    # Этот ID нужен для управления размещением
    window_frame_id = canvas.create_window((0, 0), window=scroll_frame, anchor="n")

    # Центрирование при изменении размера
    def on_canvas_resize(event):
        canvas_width = event.width
        canvas.itemconfig(window_frame_id, width=canvas_width)

    canvas.bind("<Configure>", on_canvas_resize)

    scroll_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Центрированный фрейм внутри scroll_frame
    center_frame = ttk.Frame(scroll_frame, style="White.TFrame")
    center_frame.pack(pady=20)

    transactions = report_data["transactions"]
    summary = report_data["summary"]
    categories = report_data["categories"]
    date_from = report_data["date_from"]
    date_to = report_data["date_to"]
    optional_expenses = report_data["optional_expenses"]
    report_name = report_data["report_name"]

    # --- Заголовок отчета ---
    if report_name:
        header_text = f"Отчёт: {report_name} за период от {date_from} по {date_to}"
    else:
        header_text = f"Отчёт за период от {date_from} по {date_to}"

    ttk.Label(center_frame, text=header_text, font=("Arial", 16, "bold"), style="White.TLabel").pack(pady=(20, 10))

    def add_section(title, parent):
        section = ttk.Frame(parent, style="White.TFrame")
        section.pack(fill="x", padx=20, pady=15)
        top_line = tk.Frame(section, bg="#4A90E2", height=3)
        top_line.pack(fill="x", pady=(0, 5))
        label = ttk.Label(section, text=title, font=("Arial", 13, "bold"), style="White.TLabel")
        label.pack(anchor="w", padx=10, pady=(0, 10))
        return section

    # --- Секция 1: Общий итог ---
    section1 = add_section("1. Общий итог", center_frame)

    summary_text = f"Доходы: {summary['income']}    Расходы: {summary['expenses']}    Баланс: {summary['balance']}"
    ttk.Label(section1, text=summary_text, font=("Arial", 12), style="White.TLabel").pack(pady=5)

    fig1 = Figure(figsize=(6.5, 4.5), dpi=100)
    ax1 = fig1.add_subplot(111)
    ax1.bar(["Доходы", "Расходы"], [summary['income'], summary['expenses']], color=["green", "red"])
    ax1.set_title("Доходы и Расходы")
    for i, val in enumerate([summary['income'], summary['expenses']]):
        ax1.text(i, val + max(val * 0.02, 1), str(val), ha='center', va='bottom', fontsize=10)

    chart1 = FigureCanvasTkAgg(fig1, master=section1)
    chart1.draw()
    chart1.get_tk_widget().pack()

    # --- Секция 2: Доходы по категориям ---
    section2 = add_section("2. Доходы по категориям", center_frame)

    if categories['income']:
        income_frame = ttk.Frame(section2, style="White.TFrame")
        income_frame.pack(fill="x", padx=10, pady=5)

        fig2 = Figure(figsize=(6.5, 4.5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.pie(categories['income'].values(), labels=categories['income'].keys(), autopct='%1.1f%%')
        ax2.set_title("Структура доходов")

        chart2 = FigureCanvasTkAgg(fig2, master=income_frame)
        chart2.draw()
        chart2.get_tk_widget().pack(side="left", padx=(0, 20))

        income_text_frame = ttk.Frame(income_frame, style="White.TFrame")
        income_text_frame.pack(side="left", anchor="n")

        for category, amount in categories['income'].items():
            ttk.Label(income_text_frame, text=f"{category}: {amount}", font=("Arial", 11), style="White.TLabel").pack(anchor="w")
        ttk.Label(income_text_frame, text=f"Всего доходов: {summary['income']}", font=("Arial", 11, "bold"), style="White.TLabel").pack(anchor="w", pady=(5, 0))
    else:
        ttk.Label(section2, text="Доходов за период не найдено.", font=("Arial", 11, "italic"), style="White.TLabel").pack(padx=10)

    # --- Секция 3: Расходы по категориям и подкатегориям ---
    section3 = add_section("3. Расходы по категориям и подкатегориям", center_frame)

    if categories['expenses']:
        expenses_frame = ttk.Frame(section3, style="White.TFrame")
        expenses_frame.pack(fill="x", padx=10, pady=5)

        fig3 = Figure(figsize=(6.5, 4.5), dpi=100)
        ax3 = fig3.add_subplot(111)
        ax3.pie(categories['expenses'].values(), labels=categories['expenses'].keys(), autopct='%1.1f%%')
        ax3.set_title("Структура расходов")

        chart3 = FigureCanvasTkAgg(fig3, master=expenses_frame)
        chart3.draw()
        chart3.get_tk_widget().pack(side="left", padx=(0, 20))

        expenses_text_frame = ttk.Frame(expenses_frame, style="White.TFrame")
        expenses_text_frame.pack(side="left", anchor="n")

        for category, amount in categories['expenses'].items():
            ttk.Label(expenses_text_frame, text=f"{category}: {amount}", font=("Arial", 11), style="White.TLabel").pack(anchor="w")
            subs = categories['expenses_by_sub'].get(category, {})
            for sub, sub_amount in subs.items():
                if sub and sub_amount:
                    ttk.Label(expenses_text_frame, text=f"  ↳ {sub}: {sub_amount}", font=("Arial", 10), foreground="gray", style="White.TLabel").pack(anchor="w", padx=10)
        ttk.Label(expenses_text_frame, text=f"Всего расходов: {summary['expenses']}", font=("Arial", 11, "bold"), style="White.TLabel").pack(anchor="w", pady=(5, 0))
    else:
        ttk.Label(section3, text="Расходов за период не найдено.", font=("Arial", 11, "italic"), style="White.TLabel").pack(padx=10)

    # --- Кнопки ---
    button_frame = ttk.Frame(center_frame, style="White.TFrame")
    button_frame.pack(pady=30)

    def save_to_pdf():
        print("Сохранение в PDF пока не реализовано.")

    ttk.Button(button_frame, text="Сохранить в PDF", command=save_to_pdf).pack(side="left", padx=10)
    ttk.Button(button_frame, text="Закрыть", command=window.destroy).pack(side="left", padx=10)

    def force_redraw(event=None):
        for widget in center_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                for sub in widget.winfo_children():
                    if hasattr(sub, 'draw'):
                        try:
                            sub.draw()
                        except:
                            pass

    canvas.bind_all("<MouseWheel>", force_redraw)
    canvas.bind_all("<Button-4>", force_redraw)  # для Linux
    canvas.bind_all("<Button-5>", force_redraw)