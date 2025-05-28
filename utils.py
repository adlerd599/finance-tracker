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
def validate_not_empty(value, field_name="значение"):
    if not value.strip():
        print(f'Ошибка: "{field_name}" не может быть пустым')
        return False
    return True

# Функция validate_type() проверяет корректность типов транзакций переданных как параметр
def validate_type(type_):
    if not isinstance(type_, str):
        print()
        print("Тип транзакции обязан быть строкой!")
        return
    
    if type_.lower().strip() not in ('income', 'expenses'):
        print()
        print("Ошибка: допустимые значения — 'income' или 'expenses'")
        return False
    return True

# Проверяем что data список словарей
def validate_transaction_list(data):
    if not isinstance(data, list):
        raise ValueError("Ожидался список транзакций (list)")
    
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Каждая транзакция должна быть словарем (dict)")
    