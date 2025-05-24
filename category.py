# Здесь находится основная логика управления категориями

import json
import os
from transaction import load_data, save_data
from utils import validate_not_empty, validate_type

# Создаем корректный путь к json файлу
CATEGORY_PATH = os.path.join("data", "categories.json")


# Функция load_categories() преобразует json файл в словарь и возвращает этот словарь
def load_categories():
    if not os.path.exists(CATEGORY_PATH):
        return []
    with open(CATEGORY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
    

# Функция save_categories() перезаписывает json файл новым словарем, переданным ей в качестве параметра
def save_categories(categories):
    with open(CATEGORY_PATH, "w", encoding="utf-8") as file:
        json.dump(categories, file, ensure_ascii=False, indent=2)


# Функция add_category() создает новую категорию
# В качестве параметров принимает тип транзакций, имя категории и массив с именами подкатегорий
def add_category(type_, category_name, subcategories=None):
    categories = load_categories()

    # Проверка на корректность типа транзакции
    if not validate_type(type_):
        return

    # Проверка на пустой параметр
    if not validate_not_empty(category_name, "Название категории"):
        return

    # Если тип транзакции еще не создан, то создаем его
    if type_ not in categories:
        categories[type_] = {}

    # Проверка на существование новой категории
    if category_name in categories[type_]:
        print()
        print("Ошибка: такая категория уже существует!")
        return
    
    # Если подкатегории не переданы, то создаем пустой массив
    if subcategories is None:
        subcategories = []
    else:
        # Удаляем пробелы у каждой подкатегории
        subcategories = [sub.strip() for sub in subcategories]

        # Проверяем, что нет пустых подкатегорий
        for sub in subcategories:
            if not validate_not_empty(sub):
                return
            
        # Проверяем на уникальность
        if len(subcategories) != len(set(subcategories)):
            print("Названия подкатегорий не должны повторяться!")
            return
        
    categories[type_][category_name] = subcategories
    save_categories(categories)

    print()
    print(f"Категория {category_name} добавлена!")
    if subcategories:
        print(f"А также ее подкатегории: {','.join(subcategories)}")


# Функция add_subcategory() добавляет подкатегорию в уже существующую категорию
def add_subcategory(type_, category_name, new_subcategory):
    categories = load_categories()
    new_subcategory = new_subcategory.strip()

    # Проверка на корректность типа транзакции
    if not validate_type(type_):
        return

    # Проверка на пустой параметр
    if not validate_not_empty(new_subcategory, "Название подкатегории"):
        return
    
    # Если тип транзакции еще не создан, то создаем его
    if type_ not in categories:
        categories[type_] = {}
    
    # Проверка на существование категории
    if category_name not in categories[type_]:
        print()
        print(f"Ошибка: Категория {category_name} не найдена!")
        return
    
    # Проверка на существование новой подкатегории
    if new_subcategory in categories[type_][category_name]:
        print()
        print(f"Ошибка: Подкатегория {new_subcategory} уже существует!")
        return
    
    subcategories = categories[type_][category_name]
    subcategories.append(new_subcategory)
    save_categories(categories)
    print()
    print(f" Подкатегория {new_subcategory} добавлена в категорию {category_name}.")


# Функция delete_category() удаляет категорию вместе со всеми подкатегориями
def delete_category(type_, category_name):
    categories = load_categories()
    data = load_data()
    
    if not validate_type(type_):
        return
    

    if category_name not in categories.get(type_, {}):
        print()
        print(f"Ошибка: Категория {category_name} не найдена!")
        return
    
    # Проверка наличия связанных транзакций
    for transaction in data:
        if transaction.get('type_') == type_ and transaction.get('category') == category_name:
            print()
            print(f"Невозможно удалить категорию '{category_name}': существуют связанные транзакции.")
            print("Сначала переместите или удалите соответствующие транзакции.")
            return

    # Удаление
    del categories[type_][category_name]
    save_categories(categories)

    print()
    print(f"Категория {category_name} и все ее подкатегории успешно удалены.")
    return
    


# Функция delete_subcategory() удаляет одну подкатегорию из категории.
def delete_subcategory(type_, category_name, subcategory_name):
    categories = load_categories()
    data = load_data()

    if not validate_type(type_):
        return

    # Проверяем существует ли заданная категория
    if category_name not in categories.get(type_, {}):
        print()
        print(f"Ошибка: Категория {category_name} не найдена!")
        return
    
    # Проверяем существует ли подкатегория
    if subcategory_name not in categories[type_][category_name]:
        print()
        print(f"Ошибка: подкатегория {subcategory_name} не найдена!")
        return
    
    # Проверка наличия связанных транзакций
    for transaction in data:
        if (transaction.get('type') == type_ and
            transaction.get('category') == category_name and
            transaction.get('subcategory') == subcategory_name):
            print()
            print(f"Невозможно удалить подкатегорию '{subcategory_name}': существуют связанные транзакции.")
            print("Сначала переместите или удалите соответствующие транзакции.")
            return
    
    # Удаление
    categories[type_][category_name].remove(subcategory_name)
    save_categories(categories)
    print()
    print(f"Подкатегория {subcategory_name} успешно удалена из категории {category_name}.")


# Функция rename_category() меняет имя категории.
def rename_category(type_, old_name, new_name):
    categories = load_categories()
    new_name = new_name.strip()

    # Проверка на корректность типа транзакции
    if not validate_type(type_):
        return

    # Проверка на пустой параметр
    if not validate_not_empty(new_name, "Новое название категории"):
        return

    # Проверяем существование
    if type_ not in categories:
        print()
        print(f"Ошибка: тип '{type_}' не найден.")
        return

    if old_name not in categories[type_]:
        print()
        print(f"Ошибка: Категория {old_name} не найдена!")
        return
    
    if new_name in categories[type_]:
        print()
        print(f"Ошибка: Категория {new_name} уже существует!")
        return

    # Переименование категории
    categories[type_][new_name] = categories[type_].pop(old_name)
    save_categories(categories)

    # Обновляем все транзакции
    data = load_data()
    for transaction in data:
        if transaction.get('type_') == type_ and transaction.get('category') == old_name:
            transaction['category'] = new_name
    save_data(data)

    print()
    print(f'Имя категории изменено: с "{old_name}" на "{new_name}".')
        
     
# Функция rename_subcategory() изменяет имя подкатегории
def rename_subcategory(type_, category_name, sub_old, sub_new):
    categories = load_categories()
    sub_new = sub_new.strip()

    # Проверка на корректность типа транзакции
    if not validate_type(type_):
        return

    # Проверка на пустой параметр
    if not validate_not_empty(sub_new, "Новое название подкатегории"):
        return
    
    # Проверяем существование
    if type_ not in categories:
        print()
        print(f"Ошибка: тип '{type_}' не найден.")
        return

    if category_name not in categories[type_]:
        print()
        print(f"Ошибка: Категория {category_name} не найдена!")
        return
    
    if sub_old not in categories[type_][category_name]:
        print()
        print(f"Ошибка: Подкатегория {sub_old} не найдена!")
        return
    
    # Проверка на существование новой подкатегории
    if sub_new in categories[type_][category_name]:
        print()
        print(f"Ошибка: Подкатегория {sub_new} уже существует!")
        return

    # Переименование подкатегории
    subcategories = categories[type_][category_name]
    index = subcategories.index(sub_old)
    subcategories[index] = sub_new
    save_categories(categories)

    # Обновляем все транзакции
    data = load_data()
    for transaction in data:
        if transaction.get('type_') == type_ and transaction.get('category') == category_name and transaction.get('subcategory') == sub_old:
            transaction['subcategory'] = sub_new
    save_data(data)

    print()
    print(f"Подкатегория изменена с {sub_old} на {sub_new}.")


# Перемещение транзакций
def move_transactions(type_, old_category, new_category, old_sub=None, new_sub=None):
    categories = load_categories()
    data = load_data()

    # Проверка типа транзакции
    if not validate_type(type_):
        return
    
    # Проверка существования категорий
    if type_ not in categories:
        print()
        print(f"Ошибка: Тип транзакции {type_} не существует!")
        return
    
    if old_category not in categories[type_]:
        print()
        print(f"Ошибка: Категория {old_category} не существует!")
        return
    
    if new_category not in categories[type_]:
        print()
        print(f"Ошибка: Категория {new_category} не существует!")
        return
    
    if old_sub and old_sub not in categories[type_][old_category]:
        print()
        print(f"Подкатегория {old_sub} не существует")
        return
    
    if new_sub and new_sub not in categories[type_][new_category]:
        print()
        print(f"Подкатегория {new_sub} не существует")
        return

    moved_count = 0

    for transaction in data:
        if transaction.get('type_') != type_:
            continue
        if transaction.get('category') != old_category:
            continue
        if old_sub:
            if transaction.get('subcategory') != old_sub:
                continue
        else:
            if transaction.get('subcategory'):
                continue
        transaction['category'] = new_category
        if new_sub:
            transaction['subcategory'] = new_sub
        else:
            transaction['subcategory'] = ""

        moved_count += 1

    save_data(data)
    print()
    print(f"Перемещено {moved_count} транзакций из категории '{old_category}'"
      f"{f' / {old_sub}' if old_sub else ''} в категорию '{new_category}'"
      f"{f' / {new_sub}' if new_sub else ''}")



    