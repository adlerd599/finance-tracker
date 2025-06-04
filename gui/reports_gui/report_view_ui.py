import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style as mpl_style
import numpy as np
import matplotlib.cm as cm
mpl_style.use("seaborn-v0_8-muted")  # стиль графиков

def show_report(report_data):
    window = tk.Toplevel()
    window.title("Отчёт")

    width = 1135
    height = 800

    # --- Центрирование окна ---
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

    # --- Установка белой темы для виджетов ---
    style = ttk.Style(window)
    style.configure("White.TFrame", background="white")
    style.configure("White.TLabelframe", background="white")
    style.configure("White.TLabelframe.Label", background="white")
    style.configure("White.TLabel", background="white")

    # --- Scrollable canvas ---
    canvas = tk.Canvas(window, background="white")
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Внутренний фрейм
    scroll_frame = ttk.Frame(canvas)

    # Важно: сохраняем ID окна
    window_frame_id = canvas.create_window((0, 0), window=scroll_frame, anchor="n")

    # Центрирование при ресайзе
    def on_canvas_resize(event):
        canvas_width = event.width
        # Центрируем содержимое по ширине canvas
        canvas.itemconfig(window_frame_id, width=canvas_width)

    canvas.bind("<Configure>", on_canvas_resize)

    # Обновляем scrollregion
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Центрированный frame
    center_frame = ttk.Frame(scroll_frame, style="White.TFrame", width=1000)
    center_frame.pack(expand=True, anchor='n')  # сверху, с отступом

    form = tk.Frame(center_frame)
    form.pack()

    summary = report_data["summary"]
    categories = report_data["categories"]
    date_from = report_data["date_from"]
    date_to = report_data["date_to"]
    report_name = report_data["report_name"]
    optional_expenses = report_data["optional_expenses"]

    charts_arr = []

    # --- Заголовок отчета ---
    if report_name:
        header_text = f'Отчёт: "{report_name}" (от {date_from} по {date_to})'
    else:
        header_text = f"Отчёт за период от {date_from} по {date_to}"

    tk.Label(form, text=header_text, font=("Helvetica", 14)).pack(pady=(20, 10))

    def add_section(title, parent):
        section = ttk.Frame(parent, style="White.TFrame")
        section.pack(fill="x", padx=20, pady=15)
        top_line = tk.Frame(section, bg="#4A90E2", height=3)
        top_line.pack(fill="x", pady=(0, 5))
        label = ttk.Label(section, text=title, font=("Helvetica", 13, "bold"), style="White.TLabel")
        label.pack(anchor="w", padx=10, pady=(0, 10))
        return section
    


    # === Секция 1: Общий итог ===

    section1 = add_section("1. Общий итог", form)

    content_frame_1 = ttk.Frame(section1, style="White.TFrame")
    content_frame_1.pack(fill="x", expand=True, padx=10, pady=5)

    content_frame_1.columnconfigure(0, weight=1, minsize=500)
    content_frame_1.columnconfigure(1, weight=1, minsize=400)

    left_frame_1 = ttk.Frame(content_frame_1, style="White.TFrame", width=500)
    left_frame_1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    left_frame_1.grid_propagate(False) 

    fig1 = Figure(figsize=(5.2, 3.5), dpi=100)
    ax1 = fig1.add_subplot(111)
    ax1.bar(["Доходы", "Расходы"], [summary['income'], summary['expenses']], color=["#a8d84e", "#f7252c"], width=0.7)
    ax1.set_title("Доходы и Расходы")
    max_val = max(summary['income'], summary['expenses'])
    ax1.set_ylim(0, max_val * 1.5)
    for i, val in enumerate([summary['income'], summary['expenses']]):
        ax1.text(i, val + max(val * 0.02, 1), str(val), ha='center', va='bottom', fontsize=10)

    chart1 = FigureCanvasTkAgg(fig1, master=left_frame_1)
    chart1.draw()
    chart1.get_tk_widget().pack(fill="both", expand=True)

    charts_arr = [chart1]

    right_frame_1 = ttk.Frame(content_frame_1, style="White.TFrame")
    right_frame_1.grid(row=0, column=1, sticky="nsew", padx=(50, 0))

    right_inner_1 = ttk.Frame(right_frame_1, style="White.TFrame")
    right_inner_1.place(relx=0, rely=0.5, anchor="w")

    ttk.Label(right_inner_1, text=f"Итого:", font=("Helvetica", 14, "underline"), style="White.TLabel").pack(anchor="w", pady=5)
    ttk.Label(right_inner_1, text=f"Доходы: {summary['income']}", font=("Helvetica", 12), style="White.TLabel").pack(anchor="w")
    ttk.Label(right_inner_1, text=f"Расходы: {summary['expenses']}", font=("Helvetica", 12), style="White.TLabel").pack(anchor="w")

    balance = summary["balance"]
    balance_text = f"Остаток: +{balance}" if balance > 0 else f"Остаток: {balance}"
    ttk.Label(right_inner_1, text=balance_text, font=("Helvetica", 12, "bold"), style="White.TLabel").pack(anchor="w", pady=(5, 0))



    # === Секция 2: Доходы по категориям ===

    section2 = add_section("2. Доходы по категориям", form)

    content_frame_2 = ttk.Frame(section2, style="White.TFrame")
    content_frame_2.pack(fill="x", expand=True, padx=10, pady=(30,50))

    content_frame_2.columnconfigure(0, weight=1, minsize=500)
    content_frame_2.columnconfigure(1, weight=1, minsize=400)

    if categories['income']:
        left_frame_2 = ttk.Frame(content_frame_2, style="White.TFrame", width=500)
        left_frame_2.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame_2.grid_propagate(False)

        num_sections_2 = len(categories['income'])
        colors_2 = cm.get_cmap('Set2')(np.linspace(0, 1, num_sections_2))

        fig2 = Figure(figsize=(5.2, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.pie(categories['income'].values(), labels=categories['income'].keys(), autopct='%1.1f%%', colors=colors_2)
        ax2.set_title("Структура доходов", fontsize=12, y=1.05)

        chart2 = FigureCanvasTkAgg(fig2, master=left_frame_2)
        chart2.draw()
        chart2.get_tk_widget().pack(fill="both", expand=True)

        charts_arr.append(chart2)

        right_frame_2 = ttk.Frame(content_frame_2, style="White.TFrame")
        right_frame_2.grid(row=0, column=1, sticky="nsew", padx=(50, 0))

        right_inner_2 = ttk.Frame(right_frame_2, style="White.TFrame")
        right_inner_2.place(relx=0, rely=0.5, anchor="w")

        ttk.Label(right_inner_2, text=f"Итого:", font=("Helvetica", 14, "underline"), style="White.TLabel").pack(anchor="w", pady=5)
        for category, amount in categories['income'].items():
            ttk.Label(right_inner_2, text=f"{category}: {amount}", font=("Helvetica", 12), style="White.TLabel").pack(anchor="w")
        ttk.Label(right_inner_2, text=f"Всего доходов: {summary['income']}", font=("Helvetica", 12, "bold"), style="White.TLabel").pack(anchor="w", pady=(5, 0))
    else:
        ttk.Label(content_frame_2, text="Доходов за период не найдено.", font=("Helvetica", 14, "italic"), style="White.TLabel").pack(padx=10, pady=(20,0))



   # --- Секция 3: Расходы по категориям и подкатегориям ---

    section3 = add_section("3. Расходы по категориям и подкатегориям", form)

    content_frame_3 = ttk.Frame(section3, style="White.TFrame")
    content_frame_3.pack(fill="x", expand=True, padx=10, pady=(30,50))

    content_frame_3.columnconfigure(0, weight=1, minsize=500)
    content_frame_3.columnconfigure(1, weight=1, minsize=400)

    if categories['expenses']:
        left_frame_3 = ttk.Frame(content_frame_3, style="White.TFrame", width=500)
        left_frame_3.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame_3.grid_propagate(False)

        num_sections_3 = len(categories['expenses'])
        colors_3 = cm.get_cmap('Set2')(np.linspace(0, 1, num_sections_3))

        fig3 = Figure(figsize=(5.2, 5), dpi=100)
        ax3 = fig3.add_subplot(111)
        ax3.pie(categories['expenses'].values(), labels=categories['expenses'].keys(), autopct='%1.1f%%', colors=colors_3)
        ax3.set_title("Структура расходов", fontsize=12, y=1.05)

        chart3 = FigureCanvasTkAgg(fig3, master=left_frame_3)
        chart3.draw()
        chart3.get_tk_widget().pack(fill="both", expand=True)

        charts_arr.append(chart3)

        right_frame_3 = ttk.Frame(content_frame_3, style="White.TFrame")
        right_frame_3.grid(row=0, column=1, sticky="nsew", padx=(50, 0))

        right_inner_3 = ttk.Frame(right_frame_3, style="White.TFrame")
        right_inner_3.place(relx=0, rely=0.5, anchor="w")

        ttk.Label(right_inner_3, text=f"Итого:", font=("Helvetica", 14, "underline"), style="White.TLabel").pack(anchor="w", pady=5)

        for category, amount in categories['expenses'].items():
            ttk.Label(
                right_inner_3,
                text=f"{category}: {amount}",
                font=("Helvetica", 12),
                style="White.TLabel"
            ).pack(anchor="w")

            if category == "Прочее":
                for inner_cat, inner_amount in categories.get("expenses_others_detail", {}).items():
                    ttk.Label(
                        right_inner_3,
                        text=f"  ↳ {inner_cat}: {inner_amount}",
                        font=("Helvetica", 12),
                        style="White.TLabel"
                    ).pack(anchor="w", padx=10)

                    # Ищем подкатегории для этой вложенной категории
                    subs = categories['expenses_by_sub'].get(inner_cat, {})
                    for sub, sub_amount in subs.items():
                        if sub and sub_amount:
                            ttk.Label(
                                right_inner_3,
                                text=f"    ↳ {sub}: {sub_amount}",
                                font=("Helvetica", 11),
                                foreground="gray",
                                style="White.TLabel"
                            ).pack(anchor="w", padx=20)
            else:
                subs = categories['expenses_by_sub'].get(category, {})
                for sub, sub_amount in subs.items():
                    if sub and sub_amount:
                        ttk.Label(
                            right_inner_3,
                            text=f"  ↳ {sub}: {sub_amount}",
                            font=("Helvetica", 11),
                            foreground="gray",
                            style="White.TLabel"
                        ).pack(anchor="w", padx=10)

        ttk.Label(
            right_inner_3,
            text=f"Всего расходов: {summary['expenses']}",
            font=("Helvetica", 14, "bold"),
            style="White.TLabel"
        ).pack(anchor="w", pady=(5, 0))
        ttk.Label(
                    right_inner_3,
                    text=f"    ↳ Из них необязательных: {optional_expenses}",
                    font=("Helvetica", 11),
                    foreground="gray",
                    style="White.TLabel"
                ).pack(anchor="w", padx=20)
    else:
        ttk.Label(content_frame_3, text="Расходов за период не найдено.", font=("Helvetica", 14, "italic"), style="White.TLabel").pack(padx=10, pady=(20,0))

    def create_mousewheel_handler(canvas, charts):
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            for chart in charts:
                chart.draw()
        return _on_mousewheel
    
    # --- Кнопки внизу ---
    buttons_frame = tk.Frame(form)
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Закрыть", command=window.destroy).pack(side="left")

    canvas.bind_all("<MouseWheel>", create_mousewheel_handler(canvas, charts_arr))
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux