import tkinter as tk
from tkinter import ttk, messagebox
from category import load_categories, transfer_transactions
from gui.utils_gui import show_frame

type_display = {
    'income': 'Доходы',
    'expenses': 'Расходы'
}

# Обратное соответствие:
type_reverse = {v: k for k, v in type_display.items()}

def create_move_transaction_ui(frame, data, back_callback):

    for widget in frame.winfo_children():
        widget.destroy()

    show_frame(frame, data)

    categories = load_categories()

    type_var = tk.StringVar()
    old_cat_var = tk.StringVar()
    old_sub_var = tk.StringVar()
    new_cat_var = tk.StringVar()
    new_sub_var = tk.StringVar()

    

    def update_old_categories(*args):
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')
        old_cat_cb['values'] = list(categories.get(type_, {}).keys())
        old_cat_var.set('')

    def update_old_subcategories(subs_cb):
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')
        subcats = categories.get(type_, {}).get(old_cat_var.get(), [])
        old_sub_cb['values'] = subcats
        old_sub_var.set('')

        if subcats:
            subs_cb.config(state='readonly')
        else:
            subs_cb.config(state='disabled')


    def update_new_categories(*args):
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')
        new_cat_cb['values'] = list(categories.get(type_, {}).keys())
        new_cat_var.set('')

    def update_new_subcategories(subs_cb):
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')
        subcats = categories.get(type_, {}).get(new_cat_var.get(), [])
        new_sub_cb['values'] = subcats
        new_sub_var.set('')

        if subcats:
            subs_cb.config(state='readonly')
        else:
            subs_cb.config(state='disabled')

    def handle_move():
        type_displayed = type_var.get()
        type_ = type_reverse.get(type_displayed, '')
        # type_ = type_var.get()
        old_cat = old_cat_var.get()
        new_cat = new_cat_var.get()
        old_sub = old_sub_var.get().strip() or None
        new_sub = new_sub_var.get().strip() or None

        if not type_ or not old_cat or not new_cat:
            messagebox.showerror("Ошибка", "Выберите тип и категории")
            return
        
        # Проверка обязательности подкатегорий при наличии
        if type_ == 'expenses':
            old_subs = categories.get(type_, {}).get(old_cat, [])
            new_subs = categories.get(type_, {}).get(new_cat, [])

            if old_subs and not old_sub:
                messagebox.showerror("Ошибка", "Выберите подкатегорию для старой категории.")
                return

            if new_subs and not new_sub:
                messagebox.showerror("Ошибка", "Выберите подкатегорию для новой категории.")
                return

        result = transfer_transactions(type_, old_cat, new_cat, old_sub, new_sub)
        if result["success"]:
            messagebox.showinfo("Успех", result["message"])
            back_callback()
        else:
            messagebox.showerror("Ошибка", result["message"])
        return

    def on_type_selected(event):
        update_old_categories()
        update_new_categories()

        old_cat_cb.config(state="readonly")
        new_cat_cb.config(state="readonly")

    def on_old_cat_selected(event):
        update_old_subcategories(old_sub_cb)

    def on_new_cat_selected(event):
        update_new_subcategories(new_sub_cb)


    center_wrapper = tk.Frame(frame)
    center_wrapper.pack(expand=True, anchor='n') 

    form = tk.Frame(center_wrapper)
    form.pack()

    # Настраиваем форму, чтобы колонка расширялась
    form.columnconfigure(0, weight=1)

    # --- Категория ---
    wigets_frame = tk.LabelFrame(form, text="Перевод транзакций между категориями", padx=10, pady=10, width=700, height=350)
    wigets_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
    wigets_frame.grid_propagate(False)
    wigets_frame.columnconfigure(0, weight=1)  # Чтобы содержимое могло центрироваться

    # Обёртка для колонок
    wigets_inner = tk.Frame(wigets_frame)
    wigets_inner.place(relx=0.5, rely=0.5, anchor='center')  # <-- Центрирование по вертикали и горизонтали

    # ======= Заголовок =======
    header_label_from = tk.Label(wigets_inner, text="Перевести из:", font=("Helvetica", 10, "underline"))
    header_label_from.grid(row=0, column=0, sticky="w", padx=30, pady=0)

    # Виджеты
    tk.Label(wigets_inner, text="Тип транзакции:").grid(row=1, column=0, sticky='w', padx=0, pady=5)
    type_cb = ttk.Combobox(wigets_inner, textvariable=type_var, state="readonly")
    type_cb['values'] = list(type_display.values())
    type_cb.grid(row=1, column=1, padx=0)
    type_cb.bind("<<ComboboxSelected>>", on_type_selected)

    tk.Label(wigets_inner, text="Старая категория:").grid(row=2, column=0, sticky='w', padx=0, pady=5)
    old_cat_cb = ttk.Combobox(wigets_inner, textvariable=old_cat_var, state="disabled")
    old_cat_cb.grid(row=2, column=1, padx=0)
    old_cat_cb.bind("<<ComboboxSelected>>", on_old_cat_selected)

    tk.Label(wigets_inner, text="Старая подкатегория:").grid(row=3, column=0, sticky='w', padx=0, pady=5)
    old_sub_cb = ttk.Combobox(wigets_inner, textvariable=old_sub_var, state="disabled")
    old_sub_cb.grid(row=3, column=1, padx=0)

    # ======= Заголовок =======
    header_label_to = tk.Label(wigets_inner, text="Перевести в:", font=("Helvetica", 10, "underline"))
    header_label_to.grid(row=4, column=0, sticky="w", padx=30, pady=(30, 0))

    tk.Label(wigets_inner, text="Новая категория:").grid(row=5, column=0, sticky='w', padx=0, pady=5)
    new_cat_cb = ttk.Combobox(wigets_inner, textvariable=new_cat_var, state="disabled")
    new_cat_cb.grid(row=5, column=1, padx=0)
    new_cat_cb.bind("<<ComboboxSelected>>", on_new_cat_selected)

    tk.Label(wigets_inner, text="Новая подкатегория:").grid(row=6, column=0, sticky='w', padx=0, pady=5)
    new_sub_cb = ttk.Combobox(wigets_inner, textvariable=new_sub_var, state="disabled")
    new_sub_cb.grid(row=6, column=1, padx=0)

    # --- Кнопки ---
    buttons_frame = tk.Frame(frame)
    buttons_frame.pack(pady=20)

    ttk.Button(buttons_frame, text="Переместить", command=handle_move).pack(side="left", padx=10)
    ttk.Button(buttons_frame, text="Назад", command=back_callback).pack(side="left", padx=10)

