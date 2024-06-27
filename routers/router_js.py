from fastapi import APIRouter,  HTTPException
import os
from fastapi.responses import FileResponse
from code.functions import get_directory

router = APIRouter()

dir = get_directory()

@router.get("/{script_name}")
async def get_js_file(script_name: str):
    file_path = os.path.join(dir, "jscript", f"{script_name}.js")

    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        # Если файл не найден, возвращаем ошибку 404
        raise HTTPException(status_code=404, detail="File not found")

