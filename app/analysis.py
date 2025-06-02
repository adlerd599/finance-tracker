from transaction import load_data
from datetime import datetime
from collections import defaultdict
from utils import validate_date, validate_transaction_list

# Фильтрует транзакции по дате
def filter_transactions_by_period(data, start_date, end_date):

    # Проверяем список data
    validate_transaction_list(data)

    # Проверяем, что дата начала периода корректна
    start = validate_date(start_date)
    if not start:
        return {
        "success": False,
        "message": f"Дата начала периода задана не корректно"
    }
    
    start = datetime.strptime(start, '%d-%m-%Y')

    # Проверяем, что дата конца периода задана корректно
    end = validate_date(end_date)
    if not end:
        return {
        "success": False,
        "message": "Дата конца периода задана не корректно"
    }
    
    end = datetime.strptime(end, '%d-%m-%Y')

    # Сравнение дат
    if start > end:
        return {
        "success": False,
        "message": "Дата 'от' не может быть позже даты 'до'."
    }

    # Фильтрация
    filtered_list = []
    for transaction in data:
        if start <= datetime.strptime(transaction['date'], '%d-%m-%Y') <= end:
            filtered_list.append(transaction)
        
    if not filtered_list:
        return {
        "success": False,
        "message": "Транзакции за указанный промежуток не найдены"
    }

    # Сортировка по дате (от меньшей к большей)
    sorted_list = sorted(filtered_list, key=lambda t: datetime.strptime(t['date'], '%d-%m-%Y'))

    return {
        "success": True,
        "transactions": sorted_list
    }

# Сyммирует доходы по категориям
def sum_income_by_categories(data):

    # Проверяем список data
    validate_transaction_list(data)

    # Создаем словарь со значением по умолчанию float
    result = defaultdict(float)

    # Суммируем доходы по категориям
    for transaction in data:
        if transaction.get('type_') == 'income':
            category = transaction.get('category', 'Без категории')
            result[category] += transaction.get('amount', 0)

    # Округляем и сортируем   
    rounded_result = {k: round(v, 2) for k, v in result.items()}
    sorted_result = dict(sorted(rounded_result.items(), key = lambda item: item[1], reverse=True))
    return sorted_result

# Суммирует расходы по категориям
def sum_expenses_by_categories(data):
   
    # Проверяем список data
    validate_transaction_list(data)

    # Создаем словарь со значением по умолчанию float
    result = defaultdict(float)

    # Суммируем доходы по категориям
    for transaction in data:
        if transaction.get('type_') == 'expenses':
            category = transaction.get('category', 'Без категории')
            result[category] += transaction.get('amount', 0)

    # Округляем и сортируем
    rounded_result = {k: round(v, 2) for k, v in result.items()}
    sorted_result = dict(sorted(rounded_result.items(), key = lambda item: item[1], reverse=True))
    return sorted_result
    

# Суммирует расходы по подктегориям
def sum_by_sub_for_expenses(data):

    # Проверяем список data
    validate_transaction_list(data)

    # Создаем словарь с вложенным словарем со значением по умолчанию float
    result = defaultdict(lambda: defaultdict(float))

    # Суммируем траты по подкатегориям
    for transaction in data:
        if transaction.get('type_') == 'expenses':
            cat = transaction.get('category', 'Без категории')
            sub = transaction.get('subcategory', 'Без категории')
            result[cat][sub] += transaction.get('amount', 0)

    # Округляем
    rounded_result = {
        cat: {sub: round(amount, 2) for sub, amount in subs.items()} 
        for cat, subs in result.items()
    }

    return rounded_result

# Функция которая считает сумму всех расходов и сумму необязательных расходов
def count_optional_expenses(data):

    # Проверяем список data
    validate_transaction_list(data)

    total = 0
    optional = 0

    # Проходим по словарю и суммируем нужные траты 
    for transaction in data:
        if transaction['type_'] == 'expenses':
            total += transaction.get('amount', 0)

            if transaction['optional']:
                optional += transaction.get('amount', 0)

    # Округляем
    total = round(total, 2)
    optional = round(optional, 2)
    return total, optional

# Считает все доходы 
def total_income(data):

    income = round(sum([t['amount'] for t in data if t['type_'] == 'income']), 2)
    return income

# Считает все расходы
def total_expenses(data):

    expenses = round(sum([t['amount'] for t in data if t['type_'] == 'expenses']), 2)
    return  expenses

# Считает разницу (доходы - расходы)
def total_balace(data):
    income = round(sum([t['amount'] for t in data if t['type_'] == 'income']), 2)
    expenses = round(sum([t['amount'] for t in data if t['type_'] == 'expenses']), 2)
    balance = round(income - expenses, 2)
    return balance
