# Здесь находится основнаая логика, то есть добавление и удаление транзакций, вывод их на экран,а также сохранение их в json файле.

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



# Функция list_transactions() выводит все транзакции на экран
# Если их пока нет сообщает об этом

def list_transactions():
    data = load_data()
    if not data:
        print()
        print("Пока нет транзакций.")
        return
    
    print()
    for i, item in enumerate(data, start=1):
        print(f"{i}: ID {item.get('id', '------')} | {item['date']} | {item['type_']} | {item['category']} | {item['amount']} | {item['description']}")



# Функция print_transaction() выводит подробную, хорошо читаемую информацию о транзакции
# Находит саму транзакцию по id
# Если не находит такой id то сообщает, что транзакция не найдена

def print_transaction(transaction_id):
    data = load_data()
    for item in data:
        if item.get("id") == str(transaction_id):
            print()
            print("Транзакция найдена!")
            print(f"ID: {item['id']}")
            print(f"Дата: {item['date']}")
            print(f"Сумма: {item['amount']}")
            print(f"Тип транзакции: {item['type_']}")
            if item.get('subcategory'):
                print(f"Категория: {item['category']}/{item['subcategory']}")
            else:
                print(f"Категория: {item['category']}")
            if item.get('description'):
                print(f"Описание: {item['description']}")
            if item.get('optional'):
                print(f"Обязательная трата: нет")
            else:
                print(f"Обязательная трата: да")
            return
    
    print()
    print("Ошибка: Транзакция не найдена.")



# Функция add_transaction() получает список предыдущих транзакций в data
# Добавляет в data новую транзакцию и после перезаписывает в файле старый список новым список data
# И выводит сообщение о добавлении транзакции в список

def add_transaction(amount, type_, category, subcategory="", description = "", date_str=None, optional=False):
    data = load_data()

    # Если дата передана в ручную, то она проходит валидацию на корректность
    # Если не передано ничего, то записывается сегодняшняя дата
    if date_str:
        valid_date = validate_date(date_str)
        if not valid_date:
            print("Ошибка: дата введена некорректно. Используйте формат ДД-ММ-ГГГГ.")
            return
    else:
        valid_date = datetime.now().strf("%d-%m-%Y")


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
    category_display = f"{category}/{subcategory}" if subcategory else f"{category}"
    print()
    print(f"Добавлено: {type_} - {amount} в категорию " + category_display + f", ID: {transaction_id}.")



# Функция delete_transaction(id) удаляет транзакцию по ее id в массиве data
# Если транзакция не найдена, то выводит сообщение

def delete_transaction(transaction_id):
    data = load_data()
    for i,item in enumerate(data):
        if item.get("id") == str(transaction_id):
            removed = data.pop(i)
            save_data(data)
            print()
            print(f"Удалена транзакция ID {transaction_id}: {removed["type_"]} - на сумму {removed["amount"]} от {removed["date"]}")
            return
        
    print()    
    print (f"Ошибка: Транзакция ID: {transaction_id} не найдена.")



# Функция edit_transaction() находит транзакцию по ID и позволяет изменить ее значения
# Если date или optional были введены некорректно, то функция прерывается

def edit_transaction(transaction_id):
    data = load_data()
    for transaction in data:
        if transaction.get('id') == str(transaction_id):
            print_transaction(transaction_id)
            print()
            
            # Запрос новых значений
            new_amount = input(f"Введите новую сумму: (Текущая: {transaction['amount']})").strip()
            new_type_ = input(f"Введите новый тип транзакции: (Текущий {transaction['type_']})").strip()
            new_category = input(f"Введите новую категорию: (Текущая: {transaction['category']})").strip()
            new_subcategory= input(f"Введите новую подкатегорию: (Текущая: {transaction.get('subcategory', '-')})").strip()
            new_description = input(f"Введите новое описание: (Текущее: {transaction.get('description', '-')})").strip()
            new_date = input(f"Введите новую дату: (Текущая: {transaction['date']})").strip()
            new_optional = input(f"Была ли покупка обязательной? ( Текущее: {'нет' if transaction.get('optional') else 'да'}) [да/нет]: ").strip().lower()

            # Если дата была введена, то проверяем ее на корректность, и если корректно, то перезаписываем дату
            if new_date:
                valid_date = validate_date(new_date)
                if not valid_date:
                    print()
                    print("Ошибка: дата введена некорректно. Используйте формат ДД-ММ-ГГГГ.")
                    return
                else:
                    transaction['date'] = valid_date

            # Если была изменена необходимость покупки
            if new_optional:
                if new_optional == "да":
                    transaction['optional'] = False
                elif new_optional == 'нет':
                    transaction['optional'] = True
                else:
                    print()
                    print("Ошибка: допускаются только ответ 'да' или 'нет', на вопрос о необходимости покупки!")
                    return
            
            # Обновляем переменные, если введено новое значение.
            if new_amount: transaction['amount'] = float(new_amount)
            if new_type_: transaction['type_'] = new_type_
            if new_category: transaction['category'] = new_category
            if new_subcategory: transaction['subcategory'] = new_subcategory
            if new_description: transaction['description'] = new_description
            

            save_data(data)
            return
    
    print()
    print("Ошибка: Транзакция с таким ID не найдена.")


