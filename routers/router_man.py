import os
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi import APIRouter, Request, HTTPException, Body, status
from fastapi import Response
from database.database import get_all_users, create_user, delete_user_id

from menu.parser import menu_parse
from code.functions import dir, templates
from code.auth import create_jwt

router = APIRouter()

#########################################     ФУНКЦИИ    ##############################################
# в файле работы с базой

#  все пользователи
@router.get("/userAll",  response_class=HTMLResponse)
async def read_all_users(request: Request):
    users = await get_all_users()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return templates.TemplateResponse("man_userAll.html", {"request": request, "users": users})

# новый пользователь
@router.post("/new", status_code=status.HTTP_201_CREATED)
async def add_user(username: str = Body(...), role: str = Body(...)):
    user = await create_user(username=username, password="", role=role )
    if not user:
        raise HTTPException(status_code=400, detail="Ошибка при создании пользователя.")
    return {"message": "Пользователь создан", "user_id": user.id}

# удаление пользователя
@router.delete("/del/{user_id}")
async def delete_user(user_id: int):
    deleted_user = await delete_user_id(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=200)

# перечитать меню
@router.get("/menuReload",  response_class=HTMLResponse)
async def reload(request: Request):

    path = fr'{dir}/menu'  # путь к txt=json файлам
    print ('вызов ф с путем ', {path})
    menu_parse(path)
    print('после вызова функции')
    return templates.TemplateResponse("menuReload.html", {"request": request})


# универсальный роут на выдачу man_xxx.html
@router.get("/{template}", response_class=HTMLResponse)
async def get_template(request: Request, template: str):
    template_path = os.path.join(dir, "templates", f"man_{template}.html")

    # проверка наличия шаблона
    if os.path.isfile(template_path):
        # шаблон найден
        return templates.TemplateResponse(f"man_{template}.html", {"request": request})
    else:
        # шаблон не найден
        error_message = "t:0 Template not found"
        return templates.TemplateResponse("error.html", {"request": request, "message": error_message}, status_code=404)

# универсальный роут JS
@router.get("/js/{script_name}")
async def get_js_file(script_name: str):
    file_path = os.path.join(dir, "jscript", f"man_{script_name}.js")

    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")