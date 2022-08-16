from fastapi import APIRouter, WebSocket

from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/ws",
    tags=['Websocket']
)

ten_to_lesson = [48, 9]

@router.websocket("/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket, token: str):
    await websocket.accept()

    data = get_current_user(token)
    print(token)
    print(data.id)
    print(user_id)

    if int(data.id) != user_id:
        await websocket.close(1011, "Token validation failed .")
        return
    else:
        if user_id in ten_to_lesson: 
            await websocket.send_text("O godzinie 00:00 odbędzie się lekcja przedmiotu z Imie Nazwisko.")
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    

