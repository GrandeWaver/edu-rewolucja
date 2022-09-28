from app.emails.utils import change_minute, change_subject
from  app.pusher import pusher_client
from multiprocessing import Pool
import functools
from .emails.lesson_ten_minutes import mail_student, mail_tutor
from app.utils import smap
from .database import *

class Registry():

    def __init__(self):
        # self.clients = []
        self.ten_to_lesson = []
        self.start_notification = []
        self.active_lessons = []
        # others 
    
    def reset(self):
        cursor.execute(""" SELECT id FROM users """)
        all_users = cursor.fetchall()
        for i in all_users:
            self.start_notification.append(i['id'])
    
    def return_ten_to_lesson(self):
        return self.ten_to_lesson
    
    def return_start_notification(self):
        return self.start_notification
    
    def return_active_lessons(self):
        return self.active_lessons
    

    def add_ten_to_lesson(self, tutor_id, tutor_email, tutor_firstname, tutor_lastname, student_id, student_email, student_firstname, student_lastname, lesson_time, subject, lesson_id):
        subject_changed = change_subject(subject)
        minute = change_minute(lesson_time.minute)

        row = {"tutor_id": tutor_id, "student_id": student_id, "notification": {"text": f"O godzinie {lesson_time.hour}:{minute} odbędzie się lekcja {subject_changed} z {tutor_firstname} {tutor_lastname}."}, "lesson_id": lesson_id}
        self.ten_to_lesson.append(row)

        pusher_client.trigger('alerts', str(student_id), {"text": f"O godzinie {lesson_time.hour}:{minute} odbędzie się lekcja {subject_changed} z {tutor_firstname} {tutor_lastname}."})
        pusher_client.trigger('alerts', str(tutor_id), {"text": f"O godzinie {lesson_time.hour}:{minute} odbędzie się lekcja {subject_changed} z {tutor_firstname} {tutor_lastname}."})

        mail_student_func = functools.partial(mail_student, student_email, student_firstname, tutor_firstname, tutor_lastname, subject_changed, lesson_time)
        mail_tutor_func = functools.partial(mail_tutor, tutor_email, tutor_firstname, student_firstname, student_lastname, subject_changed, lesson_time)

        with Pool() as pool:
            pool.map(smap, [mail_student_func, mail_tutor_func])
            print('wysłano powiadomienia o lekcjach')
    

    def add_active_lessons(self, lesson_id, tutor_id, tutor_firstname, tutor_lastname, tutor_picture, student_id, student_firstname, student_lastname, student_picture):
        notification = {
            "notification": "start", 
            "tutor_id": tutor_id,
            "tutor_firstname": tutor_firstname, 
            "tutor_lastname": tutor_lastname, 
            "tutor_picture": tutor_picture, 
            "student_id": student_id,
            "student_firstname": student_firstname, 
            "student_lastname": student_lastname, 
            "student_picture": student_picture
            }
        row = {"lesson_id": lesson_id, "student_id": student_id, "tutor_id": tutor_id, "notification": notification}
        self.active_lessons.append(row)

        print(f'active lessons: {len(self.active_lessons)}')

        pusher_client.trigger('videocall', str(student_id), row)
        pusher_client.trigger('videocall', str(tutor_id), row)

        # remove z ten_to_lesson TODO
    
    def remove_active_lessons(self, lesson):
        self.active_lessons.remove(lesson)
    
    def add_zoom_links(self, lesson_id, start_url, join_url):
        for index, element in enumerate(self.active_lessons):
            print(f'{lesson_id} ==? {element["lesson_id"]}')
            if element["lesson_id"] == lesson_id:
                print("[DEBUG] adding zoom links to notification")
                self.active_lessons[index].append({"start_url": start_url, "join_url": join_url, 'lesson_id': lesson_id})


registry = Registry()
registry.reset()