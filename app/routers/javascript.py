from .. import utils, schemas
from pathlib import Path
from ..database import *
from fastapi import HTTPException, Request, status, APIRouter
from starlette.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates/js')))

router = APIRouter(
    prefix="/js",
    tags=['javascript']
    )


@router.get("/utils.js")
def mainhome(request: Request):
    return templates.TemplateResponse('utils.js', {'request': request})