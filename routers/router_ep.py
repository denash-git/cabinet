import os
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import APIRouter, Request, HTTPException, Response

#from models import *  # Импорт Pydantic схем
from code.functions import dir, templates

router = APIRouter()

#####################     ФУНКЦИИ   ################################
from ldap3 import Server, Connection, ALL, SUBTREE, MODIFY_REPLACE
from starlette.concurrency import run_in_threadpool # для ldap

def connect_ldap():
    #  !!!!!  ВНИМАНИЕ !!!!! временно для теста
    server_address = 'ldap://yyyyyy.local'
    username = 'xxxxx\dm'
    password = 'xxxx123'

    # подключение к серверу
    server = Server(server_address, get_info=ALL)
    return Connection(server, username, password, auto_bind=True)

def get_users_ep():
    # базовый DN для поиска
    base_dn = 'OU=portals,OU=ЭЦП,OU=agroforce_users,DC=agroforce,DC=local'

    conn = connect_ldap()

    # поиск в указанной OU
    search_filter = '(objectClass=person)'  # фильтр
    conn.search(search_base=base_dn, search_filter=search_filter, search_scope=SUBTREE, attributes=['cn', 'sAMAccountName'])

    # get и sort результаты поиска
    users = conn.entries
    sorted_users = sorted(users, key=lambda user: user.cn.value.lower())

    # данные в виде списка словарей
    user_list = [{'cn': user.cn.value, 'sAMAccountName': user.sAMAccountName.value} for user in sorted_users]

    # end соединение
    conn.unbind()

    return user_list

def disable_user_ep(sAMAccountName: str):
    # базовый DN для поиска
    base_dn = 'OU=portals,OU=ЭЦП,OU=agroforce_users,DC=agroforce,DC=local'

    conn = connect_ldap()

    # Поиск пользователя по sAMAccountName
    search_filter = f'(sAMAccountName={sAMAccountName})'
    conn.search(search_base=base_dn, search_filter=search_filter, search_scope=SUBTREE, attributes=['userAccountControl'])

    if len(conn.entries) != 1:
        conn.unbind()
        raise ValueError(f"User with sAMAccountName {sAMAccountName} not found or multiple entries returned")

    user_dn = conn.entries[0].entry_dn
    current_uac = conn.entries[0].userAccountControl.value
    print(f"Current userAccountControl for {sAMAccountName}: {current_uac}")

    # Установка флага ACCOUNTDISABLE (0x2)
    new_uac = current_uac | 0x2
    print(f"New userAccountControl for {sAMAccountName}: {new_uac}")

    # Обновление атрибута userAccountControl
    success = conn.modify(user_dn, {'userAccountControl': [(MODIFY_REPLACE, [new_uac])]})

    if not success:
        print(f"Modification result: {conn.result}")
        conn.unbind()
        raise Exception(f"Failed to disable user: {conn.result}")

    # Завершение соединения
    conn.unbind()
    print(f"User {sAMAccountName} has been disabled successfully")

    return True
#####################################   РОУТЫ   ####################################################


# все пользователи EP
@router.get("/userAll", response_class=HTMLResponse)
async def read_users(request: Request):
    users = get_users_ep()
    return templates.TemplateResponse("ep_userAll.html", {"request": request, "users": users})

# блокировка по sAMAccount пользователя EP
# асинхронный маршрут, который вызывает синхронную функцию в отдельном потоке
@router.delete("/del/{sAMAccountName}")
async def disable_user(sAMAccountName: str):
    try:
        result = await run_in_threadpool(disable_user_ep, sAMAccountName)
        return Response(status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# -----------------------------------------------------------------

# универсальный роут /ep/xxx.html
@router.get("/{template}", response_class=HTMLResponse)
async def get_template(request: Request, template: str):
    template_path = os.path.join(dir, "templates", f"ep_{template}.html")

    # проверка наличия шаблона
    if os.path.isfile(template_path):
        # шаблон найден
        return templates.TemplateResponse(f"ep_{template}.html", {"request": request})
    else:
        # шаблон не найден
        error_message = "t:0 Template not found"
        return templates.TemplateResponse("error.html", {"request": request, "message": error_message}, status_code=404)

# JS
@router.get("/js/{script_name}")
async def get_js_file(script_name: str):
    file_path = os.path.join(dir, "jscript", f"ep_{script_name}.js")

    # проверяем, существует ли файл
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")
