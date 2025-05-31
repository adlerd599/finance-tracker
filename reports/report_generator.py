import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_expenses_by_category(transactions):
    # Группируем суммы по категориям
    category_totals = {}
    for tx in transactions:
        if tx['type'] == 'expenses':
            category = tx['category']
            category_totals[category] = category_totals.get(category, 0) + float(tx['amount'])

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(8, 6))
    plt.bar(categories, amounts, color='skyblue')
    plt.title('Расходы по категориям')
    plt.ylabel('Сумма')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    