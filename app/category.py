# Здесь находится основная логика управления категориями

import json
import os
from tkinter import messagebox
from transaction import load_data, save_data
from utils import validate_type, validate_category, validate_subcategory, validate_string

# Создаем корректный путь к json файлу
CATEGORY_PATH = os.path.join("data", "categories.json")

# Функция load_categories() преобразует json файл в словарь и возвращает этот словарь
def load_categories():
    if not os.path.exists(CATEGORY_PATH):
        return {}
    with open(CATEGORY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

# Функция save_categories() перезаписывает json файл новым словарем, переданным ей в качестве параметра
def save_categories(categories):
    with open(CATEGORY_PATH, "w", encoding="utf-8") as file:
        json.dump(categories, file, ensure_ascii=False, indent=2)

# Функция add_category() создает новую категорию
def add_category(type_, category_name):
    categories = load_categories()
    
    # Проверяем тип транзакции
    validated_type_ = validate_type(type_)
    if validated_type_:
        type_ = validated_type_

         # Если тип транзакции еще не создан, то создаем его
        if type_ not in categories:
            categories[type_] = {}
    else:
        return {
        "success": False,
        "message": "Тип транзакции передан некорректно."
        }
    
    validated_category = validate_string(category_name)
    if not validated_category:
        return {
        "success": False,
        "message": "Имя категории не может быть пустым и должно быть строкой!"
        }
    else:
        category_name = validated_category

    # Проверка на существование новой категории
    if category_name in categories[type_]:
        return {
        "success": False,
        "message": f"Категория {category_name} уже существует!"
        }
        
    categories[type_][category_name] = []
    save_categories(categories)

    return {
        "success": True,
        "message": f"Категория {category_name} добавлена!"
        }

# Функция add_subcategory() добавляет подкатегорию в уже существующую категорию
def add_subcategory(type_, category_name, new_subcategory):
    categories = load_categories()

    validated_type_ = validate_type(type_)
    # Проверяем тип транзакции
    if validated_type_:
        type_ = validated_type_

        # Если тип транзакции еще не создан, то создаем его
        if type_ not in categories:
            return {
                "success": False,
                "message": f"Тип транзакции {type_} не существует!"
            }

        # Проверяем имя категории
        validated_category = validate_category(categories, type_, category_name)
        if validated_category:
            category_name = validated_category
        else:
            return {
            "success": False,
            "message": "Категория передана некорректно."
            }
    else:
        return {
        "success": False,
        "message": "Тип транзакции передан некорректно."
        }
    
    validated_subcategory = validate_string(new_subcategory)
    if not validated_subcategory:
        return {
        "success": False,
        "message": "Имя подкатегории не может быть пустым и должно быть строкой!"
        }
    else:
        new_subcategory = validated_subcategory

    # Проверка на существование новой подкатегории
    if new_subcategory in categories[type_][category_name]:
        return {
        "success": False,
        "message": f"Подкатегория {new_subcategory} уже существует!"
        }
    
    subcategories = categories[type_][category_name]
    subcategories.append(new_subcategory)
    save_categories(categories)
    return {
        "success": True,
        "message": f"Подкатегория {new_subcategory} добавлена в категорию {category_name}."
        }

# Функция delete_category() удаляет категорию вместе со всеми подкатегориями
def delete_category(type_, category_name):
    data = load_data()
    categories = load_categories()

   # Проверяем тип транзакции
    validated_type = validate_type(type_)
    if validated_type:
        type_ = validated_type

        # Проверяем имя категории
        validated_category = validate_category(categories, type_, category_name)
        if validated_category:
            category_name = validated_category
        else:
            return {
            "success": False,
            "message": "Категория передана некорректно."
            }
    else:
        return {
        "success": False,
        "message": "Тип транзакции передан некорректно."
        }
    
    # Проверка наличия связанных транзакций
    for transaction in data:
        if transaction.get('type_') == type_ and transaction.get('category') == category_name:
             return {
                "success": False,
                "message":  f"Невозможно удалить категорию '{category_name}': \nСуществуют связанные транзакции."
                            f"\nСначала переместите или удалите соответствующие транзакции."
                }
    
    confirm = messagebox.askyesno(
    'Подтверждение',
    f'Вы уверены, что хотите полностью удалить категорию "{category_name}"?'
    )
    if not confirm:
        return
    
    # Удаление
    del categories[type_][category_name]
    save_categories(categories)

    return {
            "success": True,
            "message": f"Категория {category_name} и все ее подкатегории успешно удалены."
            }

# Функция delete_subcategory() удаляет одну подкатегорию из категории.
def delete_subcategory(type_, category_name, subcategory_name):
    data = load_data()
    categories = load_categories()

    # Проверяем тип транзакции
    validated_type = validate_type(type_)
    if validated_type:
        type_ = validated_type

        # Проверяем имя категории
        validated_category = validate_category(categories, type_, category_name)
        if validated_category:
            category_name = validated_category

            validated_subcategory = validate_subcategory(categories, type_, category_name, subcategory_name)
            if validated_subcategory:
                subcategory_name = validated_subcategory
            else:
                 return {
                "success": False,
                "message": "Подкатегория передана некорректно."
                }
        else:
            return {
            "success": False,
            "message": "Категория передана некорректно."
            }
    else:
        return {
        "success": False,
        "message": "Тип транзакции передан некорректно."
        }
    
    # Проверка наличия связанных транзакций
    for transaction in data:
        if (transaction.get('type_') == type_ and
            transaction.get('category') == category_name and
            transaction.get('subcategory') == subcategory_name):
            return {
            "success": False,
            "message":  f"Невозможно удалить подкатегорию '{subcategory_name}': \nCуществуют связанные транзакции."
                        "\nСначала переместите или удалите соответствующие транзакции."
            }
    
    confirm = messagebox.askyesno(
    'Подтверждение',
    f'Вы уверены, что хотите удалить подкатегорию "{subcategory_name}" из категории "{category_name}"?'
    )
    if not confirm:
        return

    # Удаление
    categories[type_][category_name].remove(subcategory_name)
    save_categories(categories)

    return {
        "success": True,
        "message": f"Подкатегория {subcategory_name} успешно удалена из категории {category_name}."
        }

# Функция rename_category() меняет имя категории.
def rename_category(type_, old_name, new_name):
    data = load_data()
    categories = load_categories()

    # Проверяем тип транзакции
    validated_type = validate_type(type_)
    if validated_type:
        type_ = validated_type

        # Проверяем имя категории
        validated_category = validate_category(categories, type_, old_name)
        if validated_category:
            old_name = validated_category
        else:
            return {
            "success": False,
            "message": "Категория передана некорректно."
            }
    else:
        return {
        "success": False,
        "message": "Тип транзакции передан некорректно."
        }
    
    validated_new_name = validate_string(new_name)
    if not validated_new_name:
        return {
        "success": False,
        "message": "Новое название категории не может быть пустым и должно быть строкой."
        }
    else:
        new_name = validated_new_name
    
    if new_name in categories[type_]:
        return {
        "success": False,
        "message": f"Категория {new_name} уже существует!."
        }

    # Переименование категории
    categories[type_][new_name] = categories[type_].pop(old_name)
    save_categories(categories)

    # Обновляем все транзакции
    for transaction in data:
        if transaction.get('type_') == type_ and transaction.get('category') == old_name:
            transaction['category'] = new_name
    save_data(data)

    return {
        "success": True,
        "message": f"Имя категории изменено: с '{old_name}' на '{new_name}'."
        }
    
# Функция rename_subcategory() изменяет имя подкатегории
def rename_subcategory(type_, category_name, sub_old, sub_new):
    data = load_data()
    categories = load_categories()

    # Проверяем тип транзакции
    validated_type_ = validate_type(type_)
    if validated_type_:
        type_ = validated_type_

        # Проверяем имя категории
        validated_category = validate_category(categories, type_, category_name)
        if validated_category:
            category_name = validated_category

            validated_sub_old = validate_subcategory(categories, type_, category_name, sub_old)
            if validated_sub_old:
                sub_old = validated_sub_old
            else:
                 return {
                "success": False,
                "message": "Подкатегория передана некорректно."
                }
        else:
            return {
            "success": False,
            "message": "Категория передана некорректно."
            }
    else:
        return {
        "success": False,
        "message": "Тип транзакции передан некорректно."
        }
    
    validated_sub_new = validate_string(sub_new)
    if not validated_sub_new:
        return {
        "success": False,
        "message": "Новое название категории не может быть пустым и должно быть строкой."
        }
    else:
        sub_new = validated_sub_new
    
    # Проверка на существование новой подкатегории
    if sub_new in categories[type_][category_name]:
        return {
        "success": False,
        "message": f"Подкатегория {sub_new} уже существует!."
        }

    # Переименование подкатегории
    subcategories = categories[type_][category_name]
    index = subcategories.index(sub_old)
    subcategories[index] = sub_new
    save_categories(categories)

    # Обновляем все транзакции
    for transaction in data:
        if (transaction.get('type_') == type_ 
            and transaction.get('category') == category_name 
            and transaction.get('subcategory') == sub_old):
            transaction['subcategory'] = sub_new
    save_data(data)

    return {
        "success": True,
        "message": f"Имя подкатегории изменено: с '{sub_old}' на '{sub_new}'."
        }

# Перемещает все транзакции из одной категории/подкатегории в другую
def transfer_transactions(type_, old_category, new_category, old_sub=None, new_sub=None):
    data = load_data()
    categories = load_categories()

    # Проверяем тип транзакции
    validated_type_ = validate_type(type_)
    if validated_type_:
        type_ = validated_type_

        # Проверяем имя категории
        validated_old_category = validate_category(categories, type_, old_category)
        if validated_old_category:
            old_category = validated_old_category

            if old_sub:
                validated_old_sub = validate_subcategory(categories, type_, old_category, old_sub)
                if validated_old_sub:
                    old_sub = validated_old_sub
                else:
                    return {
                    "success": False,
                    "message": "Прежняя подкатегория передана некорректно."
                    }
        else:
            return {
            "success": False,
            "message": "Прежняя категория передана некорректно."
            }
        
        validated_new_category = validate_category(categories, type_, new_category)
        if validated_new_category:
            new_category = validated_new_category

            if new_sub:
                validated_new_sub = validate_subcategory(categories, type_, new_category, new_sub)
                if validated_new_sub:
                    new_sub = validated_new_sub
                else:
                    return {
                    "success": False,
                    "message": "Новая подкатегория передана некорректно."
                    }
        else:
            return {
            "success": False,
            "message": "Новая категория передана некорректно."
            }
    else:
        return {
        "success": False,
        "message": "Тип транзакции передан некорректно."
        }
    
    if old_category == new_category and old_sub == new_sub:
        return {
        "success": False,
        "message": "Категории и подкатегории совпадают!"
        }
    
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

    if moved_count == 0:
        return {
        "success": False,
        "message": "Транзакций в изначальной категории/подкатегории не обнаружено."
        }
    else:
        save_data(data)
        return {
        "success": True,
        "message": f"Перемещено {moved_count} транзакций из категории '{old_category}'"
            f"{f' / {old_sub}' if old_sub else ''} в категорию '{new_category}'"
            f"{f' / {new_sub}' if new_sub else ''}"
        }



    