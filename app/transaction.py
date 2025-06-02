# Здесь находится основнаая логика транзакций, то есть добавление, измененме и удаление транзакций

# Модуль os используется для работы с путями файлов и папок, и проверки существует ли файл.
import os 
import json
from datetime import datetime
from utils import generate_transaction_id, validate_date

# Это функция из модуля os, которая соединяет части пути (папки, имена файлов) так, как это принято в операционной системе, на которой работает программа.
DATA_FILE = os.path.join("data", "finance_data.json")

# Функция load_data() получает список со всеми операциями.
# Сначала проверяет существует ли файл DATA_FILE, если нет - то возвращает пустой массив.
# А если существует, то безопасно открывает его ("r" - режим чтения, "utf-8" - для русских символов) и возвращает список с эл-ми словаря из json файла.
def load_data(): 
    if not os.path.exists(DATA_FILE): 
        return [] 
    with open(DATA_FILE, "r", encoding="utf-8") as file: 
        return json.load(file) 

# Функция save_data() открывает файл в режиме записи "w" 
# Перезаписывает его новым списком data 
# ensure_ascii=False -для русских символов
# indent=2 для отступов, без этого сохраняет в одну строку
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# Функция add_transaction() получает список предыдущих транзакций в data
# Добавляет в data новую транзакцию и после перезаписывает в файле старый список новым список data
# И выводит сообщение о добавлении транзакции в список
def add_transaction(amount, type_, category, subcategory="", description = "", date_str=None, optional=False):
    data = load_data()

    # Если не передано ничего, то записывается сегодняшняя дата
    if date_str:
        valid_date = date_str
    else:
        valid_date = datetime.now().strftime("%d-%m-%Y")


    # Генерация нового ID
    existing_ids = {t["id"] for t in data if "id" in t} # Множество уникальных id, которые уже принадлежат какой-либо транзакции.
    transaction_id = generate_transaction_id(existing_ids)

    transaction = {
        "id": transaction_id,
        "date": valid_date,
        "amount" : amount,
        "type_": type_,
        "category": category,
        "subcategory": subcategory,
        "description": description,
        "optional": optional
    }

    data.append(transaction)
    save_data(data)

# Функция delete_transaction(id) удаляет транзакцию по ее id в массиве data
# Если транзакция не найдена, то выводит сообщение
def delete_transaction(transaction_id):
    data = load_data()
    for i,item in enumerate(data):
        item_id = int(item.get("id"))
        if item_id == int(transaction_id):
            removed = data.pop(i)

            type_map = {
                'expenses': 'Расходы',
                'income': 'Доходы'
            }

            type_of_transactions = type_map.get(removed.get('type_'), 'Неизвестно')

            save_data(data)
            return {
                "success": True,
                "message": f"Удалена транзакция ID {transaction_id} - на сумму {removed['amount']} от {removed['date']} \nТип: {type_of_transactions}, Категория: {removed['category']}"
            }
        
    return {
        "success": False,
        "message": f"Транзакция ID {transaction_id} не найдена."
    }

# Редактирование транзакции
def update_transaction_by_id(transaction_id, updates):
    data = load_data()

    for transaction in data:
        if str(transaction.get('id')) == str(transaction_id):
            for key, value in updates.items():
                if key == "amount":
                    try:
                        transaction["amount"] = float(value)
                    except ValueError:
                        return {
                            "success": False,
                            "message": "Сумма должна быть числом."
                        }
                elif key == "date":
                    valid_date = validate_date(value)
                    if not valid_date:
                        return {
                            "success": False,
                            "message": "Неверный формат даты. Используйте ДД-ММ-ГГГГ."
                        }
                    transaction["date"] = valid_date
                elif key == "optional":
                    if isinstance(value, bool):
                        transaction["optional"] = value
                    else:
                        return {
                            "success": False,
                            "message": "Поле optional должно быть True или False."
                        }
                else:
                    # Для всех остальных полей просто обновляем
                    transaction[key] = value
    
            save_data(data)
            return {
                    "success": True,
                    "message": f"Транзакция ID {transaction_id} успешно обновлена.",
                    "updated_transaction": transaction
                }
        
    return {
        "success": False,
        "message": f"Транзакция ID {transaction_id} не найдена."
    }