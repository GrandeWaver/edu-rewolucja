from fastapi import FastAPI, APIRouter

from app.routers.auth import auth
from .routers import frontend, resources, user, post, auth, class_


app = FastAPI()
app.include_router(frontend.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(class_.router)
app.include_router(auth.router)
app.include_router(resources.router)





