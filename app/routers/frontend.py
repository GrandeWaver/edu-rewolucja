from pathlib import Path
from fastapi import APIRouter, HTTPException, Request, status
from starlette.templating import Jinja2Templates
from ..database import *
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

router = APIRouter(
    prefix="",
    tags=['Frontend']
)

@router.get("/")
def testing():
    path =str(Path(BASE_DIR, 'templates'))
    file_path = os.path.join(path, 'index.html')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")


# @router.get("/app")
# def mainhome(request: Request):
#     return templates.TemplateResponse('VueIndex.html', {'request': request})

# @router.get("/")
# def mainhome(request: Request):
#     return templates.TemplateResponse('index.html', {'request': request})


@router.get("/testing")
def testing():
    path =str(Path(BASE_DIR, 'templates'))
    file_path = os.path.join(path, 'testing.html')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")


@router.get("/signup")
def signup():
    path =str(Path(BASE_DIR, 'templates'))
    file_path = os.path.join(path, 'signup.html')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")


@router.get("/signin")
def signup():
    path =str(Path(BASE_DIR, 'templates'))
    file_path = os.path.join(path, 'signin.html')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")


@router.get("/welcomeback")
def signup():
    path =str(Path(BASE_DIR, 'templates'))
    file_path = os.path.join(path, 'welcomeback.html')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")



