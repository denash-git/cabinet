import json

def menu_parse(dir):
    menu = [] # словарь под меню
    menu_current = None

    with open(fr'{dir}\menu.ini', 'r', encoding='utf-8') as file:
        for line in file:

            # исключаем пустые строки и комментарии
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split() # дробим строку на части, удаляя лишние пробелы
            
            # если первый символ +, то это главный пункт меню с ролью
            if parts[0] == '+':
                if len(parts) >= 3:
                    role = parts[-1]  # последний элемент - роль
                    menu_title = ' '.join(parts[1:-1])  # все остальное - заголовок меню
                    menu_current = {'title': menu_title, 'role': role, 'subitems': []}
                    menu.append(menu_current)
                else:
                    print('m:0 invalid menu structure')
            # если первый символ -, то это подпункт текущего главного меню
            elif parts[0] == '-':
                if len(parts) >= 3:
                    url = parts[-1]  # последний элемент - url
                    title = ' '.join(parts[1:-1])  # все остальное - подпункт
                    menu_current['subitems'].append({'title': title, 'url': url})
                else:
                    print('m:0 invalid menu structure')

    # menu сформировано как словарь, сохраняем как json
    menu_json = json.dumps(menu, indent=4, ensure_ascii=False)
    with open(fr'{dir}\menu.json', 'w', encoding='utf-8') as file:
        file.write(menu_json)

    return

#UNIT TEST
if __name__ == '__main__':
    import json
    import os

    # текущая директория
    dir = os.path.dirname(os.path.realpath(__file__))
    menu_parse(fr'{dir}')
    print('Выполнено')
