from pathlib import Path
from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

router = APIRouter(
    prefix="",
    tags=['Frontend']
)


@router.get("/")
def mainhome(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})