import os
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi import APIRouter, Request, HTTPException, Depends, status
from database.database import create_tables, authenticate_user, register_user
from code.functions import dir, templates, menu_load
from code.models import UserValid # Импорт Pydantic схем
from code.auth import get_current_user, create_jwt

router = APIRouter()


print('log: hабочая директория: ', dir)


# Первичное создание таблицы в базе
@router.on_event("startup")
async def startup_event():
    await create_tables()

# страница авторизации, 1 стр
@router.get("/",  response_class=HTMLResponse)
async def get_auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@router.get("/favicon.ico", include_in_schema=False)
async def read_favicon():
    path = f'{dir}/templates/favicon.ico'
    return FileResponse(path)

@router.get("/menu", response_class=HTMLResponse)
async def get_menu(request: Request, user: dict = Depends(get_current_user)):
        # роль обратившегося
        role = user.role
        # формирование меню по роли
        menu = menu_load(role)

        # формирование из шаблона
        return templates.TemplateResponse("sidebar.html", {"request": request, "menu": menu})

# ------------------------------     обработка с форм  ----------------------

# авторизация, приходит с формы auth
@router.post("/token", status_code=status.HTTP_200_OK)
async def auth(user: UserValid):
    user_data = await authenticate_user(user.username, user.password)
    if user_data:
        # ген JWT с полезной нагрузкой
        jwe_token = create_jwt(user_data)
        # отправляем JWT пользователю

        #  проблема ! пока не происходит редиректа
        response = RedirectResponse(url="/board", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="jwe_token", value=f"Bearer {jwe_token}", httponly=True)

        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


# регистрация пользователя, приходит с формы register
@router.post("/reg", status_code=status.HTTP_201_CREATED)
async def register(user: UserValid):
    registered_user = await register_user(user.username, user.password)
    if registered_user:
        return {"message": "User registered successfully", "user_id": registered_user.id}
    else:
        raise HTTPException(status_code=400, detail="User registration failed")

# -------------------------------------------------------------------------------------

# Универсальный роут на выдачу .html
@router.get("/{template}", response_class=HTMLResponse)
async def get_template(request: Request, template: str):
    template_path = os.path.join(dir, "templates", f"{template}.html")
    #print('extact Role user: ', user.role)
    # проверка наличия шаблона
    if os.path.isfile(template_path):
        # шаблон найден
        return templates.TemplateResponse(f"{template}.html", {"request": request})
    else:
        # шаблон не найден
        error_message = "t:0 Template not found"
        return templates.TemplateResponse("error.html", {"request": request, "message": error_message}, status_code=404)