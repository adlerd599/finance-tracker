import sys
import os
import shutil
from app.utils import get_base_path

BASE_DIR = get_base_path()
DATA_DIR = os.path.join(BASE_DIR, "data")

# Копируем встроенные json из архива PyInstaller во внешнюю папку, если их ещё нет
def extract_data_files():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    built_in_data_dir = os.path.join(sys._MEIPASS, "data") if getattr(sys, 'frozen', False) else os.path.join(BASE_DIR, "data")

    for filename in ["finance_data.json", "categories.json"]:
        src = os.path.join(built_in_data_dir, filename)
        dst = os.path.join(DATA_DIR, filename)
        if not os.path.exists(dst):
            try:
                shutil.copyfile(src, dst)
            except Exception as e:
                print(f"Ошибка при копировании {filename}: {e}")

# Выполнить копирование при запуске
extract_data_files()

# Глобальные пути
DATA_FILE = os.path.join(DATA_DIR, "finance_data.json")
CATEGORY_PATH = os.path.join(DATA_DIR, "categories.json")

# Запуск GUI
from gui.main_gui import run_gui

print("DATA_FILE:", DATA_FILE)
print("CATEGORY_PATH:", CATEGORY_PATH)

if __name__ == "__main__":
    run_gui()