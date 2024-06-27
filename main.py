from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
import uvicorn
from routers.router import router
from routers.router_man import router as router_man
from routers.router_ep import router as router_ep
from code.auth import access_control, get_current_user

app = FastAPI()

@app.middleware("http")
async def role_based_access_control(request: Request, call_next):
    # запрашиваемый роут
    path = request.url.path
    # вырезаем префикс
    end = path.find('/', 1)
    prefix = path[0:end if end != -1 else None]

    # сответствующие пути разрешения
    allowed_roles = access_control[prefix]

    # обработка не аутентифицированных
    if "public" in allowed_roles:
        return await call_next(request)

    # аутентификация
    try:
        user = await get_current_user(request)
    except HTTPException as e:
        #raise HTTPException(status_code=e.status_code, detail=e.detail)
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            # Выполнить редирект на страницу авторизации
            return RedirectResponse(url="/")
        else:
            # Возврат стандартного ответа об ошибке
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    # далее обработка только аутентифицированных, появляется user и role

    # одобрение с любыми правами
    if "all" in allowed_roles:
        return await call_next(request)

    # если найденных * подходящих нет, то ищем точные пути
    if user.role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: Insufficient role")

    response = await call_next(request)
    return response


app.include_router(router)
app.include_router(router_ep, prefix="/ep")
app.include_router(router_man, prefix="/man")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5001, reload=True)

    # uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
