from fastapi import Depends, HTTPException, status, APIRouter
from app.emails.utils import change_minute, change_subject
from app.emails.zoom_deactivation import zoom_deactivation
from  app.pusher import pusher_client

from app import oauth2
from app.registry import registry

router = APIRouter(
    prefix="/notifications",
    tags=['Notifications']
    )

@router.get('/')
def get_notifications(user_data = Depends(oauth2.get_current_user)):
        # check from registry czy nie ma jakiś powiadomień. które powinien zwrócić
        start_notification = registry.return_start_notification()
        ten_to_lesson = registry.return_ten_to_lesson()
        active_lessons = registry.return_active_lessons()
        user_id = int(user_data.id)

        final_response = {"status": "success"}

        if user_id in start_notification:
                pusher_client.trigger('alerts', str(user_data.id), {"text": f"Strona w trakcie budowy. Nie wszystko może działać poprawnie."})
                #usun sie z registry jako ze już odebrałeś powiadomienie
                start_notification.remove(user_id)

        for i in ten_to_lesson:
                if user_id == i['tutor_id'] or user_id == i['student_id']:
                        pusher_client.trigger('alerts', str(user_id), i['notification'])

        for i in active_lessons:
                if user_id == i['tutor_id'] or user_id == i['student_id']:
                        # pusher_client.trigger('videocall', str(user_id), i['notification'])
                        final_response = i

        # others notifications

        return final_response

@router.post('/zoom/deauthorization')
def get_notifications():
        zoom_deactivation()

        return {"status": "success"}






        