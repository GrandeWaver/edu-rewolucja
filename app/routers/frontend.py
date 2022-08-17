from pathlib import Path
from fastapi import APIRouter, HTTPException, Request, status, Depends
from starlette.templating import Jinja2Templates
from app.pusher import pusher_client

from app import oauth2
from ..database import *
from fastapi.responses import FileResponse
import pusher

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

router = APIRouter(
    prefix="",
    tags=['undefined']
)

@router.get("/favicon.ico")
def favicon():
    path =str(Path(BASE_DIR, 'images'))
    file_path = os.path.join(path, 'favicon.png')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")


@router.post("/alert")
def testing(message: str):
    pusher_client.trigger('alerts', 'main', {'text': message})


# @router.get("/admin")
# def admin(user_data = Depends(oauth2.get_current_user)):
#     if user_data.id != 1:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Only for the boss")

#     path =str(Path(BASE_DIR, 'admin'))
#     file_path = os.path.join(path, 'index.html')
#     if os.path.exists(file_path):
#         return FileResponse(file_path)
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found")


