# Здесь находятся разные вспомогательные функции

import random
import re
from datetime import datetime

# Функция validate_date() проверяет корректность введенной даты. Допускает любые разделители
# Возвращает дату в формате ДД-ММ-ГГГГ или None если дата некорретна
def validate_date(date_str):
    # Очищаем строку от пробелов и заменяем любые разделительные символы на "-"
    cleaned = re.sub(r"[^0-9a-zA-Z]+", "-", date_str.strip())

    try:
        # Пытаемся разобрать как дату в формате ДД-ММ-ГГГГ
        parsed_date = datetime.strptime(cleaned,"%d-%m-%Y")

        # Проверка диапазона года
        year = parsed_date.year
        current_year = datetime.now().year
        if not (1970 <= year <= current_year):
            return None
        
        return parsed_date.strftime("%d-%m-%Y")
    # Если дата введена некорректно, то возвращает None
    except ValueError:
        return None

# Функция generate_transaction_id() - генерирует случайное 6-значное число
# Проверяет, что это число не является id никакой другой транзакции
# Возвращает 6-значный уникальный номер id
def generate_transaction_id(existing_ids):
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing_ids:
            return new_id

# Функция validate_not_empty() проверяет, что строка не пустая и не состоит только из пробелов
# Возвращает True, если строка валидна, иначе печатает сообщение и возвращает False
def validate_not_empty(value):
    return isinstance(value, str) and bool(value.strip())

def validate_string(value):
    if not isinstance(value, str) or not value.strip():
        return False
    return value.strip().capitalize()

# Функция validate_type() проверяет корректность типов транзакций переданных как параметр
def validate_type(type_):

    if not validate_not_empty(type_):
        return False
    
    type_ = type_.strip().lower()
    if type_ not in ('income', 'expenses'):
        return False
    
    return type_

# Проверяет категорию на корректность ввода и существование
# Возвращает имя категории без отступов
def validate_category(categories, type_, category):

    validated_category = validate_string(category)
    if not validated_category:
        return False
    else:
        category = validated_category
    
    if category not in categories[type_]:
        return False 
    
    return category

# Проверяем подкатегории
def validate_subcategory(categories, type_, category, subcategory):

    if not validate_string(subcategory):
        return False
    else:
        subcategory = validate_string(subcategory)

    if not subcategory in categories[type_][category]:
        return False
    
    return subcategory 

# Проверяем что data список словарей
def validate_transaction_list(data):
    if not isinstance(data, list):
        raise ValueError("Ожидался список транзакций (list)")
    
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Каждая транзакция должна быть словарем (dict)")
    