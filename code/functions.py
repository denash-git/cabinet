import os, sys, json
import bcrypt
from fastapi.templating import Jinja2Templates


# директория скрипта
def get_directory():
    return os.path.dirname(os.path.abspath(sys.argv[0]))
dir = get_directory()

def get_templates():
    dir = get_directory()
    return Jinja2Templates(directory=os.path.join(dir, "templates"))
templates = get_templates()

def password_hash(password: str) -> str:
    # генерация
    salt = bcrypt.gensalt()
    # хеширование пароля
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# проверка пароля
def password_verify(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# выборка меню по роли в запросе
def menu_load(role):

    # меню подгружается из файла
    menu_file_path = fr'{dir}/menu/menu.json'

    try:
        with open(menu_file_path, "r", encoding="utf-8") as file:
            menu_data = json.load(file)

        if role == "root":
            # возврат всего меню для root
            return menu_data

        if role == "admin":
            # все для админа, кроме "root"
            menu_filter = [
                menu_item for menu_item in menu_data if menu_item["role"] != "root"
            ]
            return menu_filter
        else:
            # фильтруем пункты меню по роли пользователя
            menu_filter = [
                menu_item for menu_item in menu_data if menu_item["role"] == role
            ]
            return menu_filter

    except FileNotFoundError:
        print(f"Меню файл не найден по пути {menu_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле {menu_file_path}")
        return []
