from .. import utils, schemas
from pathlib import Path
from ..database import *
from fastapi import HTTPException, Request, status, APIRouter
from starlette.templating import Jinja2Templates
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).resolve().parent
path =str(Path(BASE_DIR, 'templates/v2'))
# templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates/resources')))

router = APIRouter(
    prefix="/v2",
    tags=['v2']
    )

# @router.get("/style.css")
# def style():
#     file_path = os.path.join(path, 'style.css')
#     if os.path.exists(file_path):
#         return FileResponse(file_path)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")

# @router.get("/vue.js")
# def vue():
#     file_path = os.path.join(path, 'vue.js')
#     if os.path.exists(file_path):
#         return FileResponse(file_path)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")

# @router.get("/utils.js")
# def utils():
#     file_path = os.path.join(path, 'utils.js')
#     if os.path.exists(file_path):
#         return FileResponse(file_path)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")

@router.get("/")
def v2():
    file_path = os.path.join(path, 'v2.html')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")

@router.get("/signin")
def signup():
    file_path = os.path.join(path, 'signin.html')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")


@router.get("/style.css")
def style():
    file_path = os.path.join(path, 'style.css')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")