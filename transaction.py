import json
import random
from datetime import datetime

# Модуль os используется для работы с путями файлов и папок, и проверки существует ли файл.
import os 

# Это функция из модуля os, которая соединяет части пути (папки, имена файлов) так, как это принято в операционной системе, на которой работает программа.
DATA_FILE = os.path.join("data", "finance_data.json")



# Функция load_data() получает список со всеми операциями.
# Сначала проверяет существует ли файл DATA_FILE, если нет - то возвпащает пустой массив.
# А если существует, то безопасно открывает его ("r" - режим чиения, "utf-8" - для русских символов) и возвращает список с эл-ми словаря из json файла.

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



# Функция generate_transaction_id() - генерирует случайное 6-значное число
# Проверяет, что это число не является id никакой другой транзакции
# Возвращает 6-значный уникальный номер id

def generate_transaction_id(existing_ids):
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing_ids:
            return new_id



# Функция list_transactions() выводит все транзакции на экран
# Если их пока нет сообщает об этом

def list_transactions():
    data = load_data()
    if not data:
        print("Пока нет транзакций")
        return
    
    for i, item in enumerate(data, start=1):
        print(f"{i}: ID {item.get('id', '------')} | {item['date']} | {item['type_']} | {item['category']} | {item['amount']} | {item['description']}")


# Функция add_transaction() получает список предыдущих транзакций в data
# Добавляет в data новую транзакцию и после перезаписывает в файле старый список новым список data
# И выводит сообщение о добавлении транзакции в список

def add_transaction(amount, category, type_, description = ""):
    data = load_data()
    existing_ids = {t["id"] for t in data if "id" in t} # Множество уникальных id, которые уже принадлежат какой-либо транзакции.
    transaction_id = generate_transaction_id(existing_ids)

    transaction = {
        "amount" : amount,
        "category": category,
        "type_": type_,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "id": transaction_id
    }
    data.append(transaction)
    save_data(data)
    print(f"Добавлено: {type_} - {amount} в категорию {category}, ID: {transaction_id}")



# Функция delete_transaction(id) удаляет транзакцию по ее id в массиве data
# Если транзакция не найдена, то выводит сообщение

def delete_transaction(transaction_id):
    data = load_data()
    for i,item in enumerate(data):
        if item.get("id") == str(transaction_id):
            removed = data.pop(i)
            save_data(data)
            print(f"Удалена транзакция ID {transaction_id}: {removed["type_"]} - на сумму {removed["amount"]} от {removed["date"]}")
            return
    print (f"Транзакция ID: {transaction_id} не найдена")