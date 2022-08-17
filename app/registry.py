from app.emails.utils import change_minute, change_subject
from  app.pusher import pusher_client
from multiprocessing import Pool
import functools
from .emails.lesson_ten_minutes import mail_student, mail_tutor
from app.utils import smap

class Registry():

    def __init__(self):
        self.clients = []
        self.ten_to_lesson = []
        # others 
    
    def add_ten_to_lesson(self, tutor_id, tutor_email, tutor_firstname, tutor_lastname, student_id, student_email, student_firstname, student_lastname, lesson_time, subject):
        # row = {"user_id": user_id, "lesson_time": lesson_time, "subject": subject, "tutor_firstname": tutor_firstname, "tutor_lastname": tutor_lastname}
        # self.ten_to_lesson.append(row)

        subject_changed = change_subject(subject)
        minute = change_minute(lesson_time.minute)

        pusher_client.trigger('alerts', str(student_id), {"text": f"O godzinie {lesson_time.hour}:{minute} odbędzie się lekcja {subject_changed} z {tutor_firstname} {tutor_lastname}."})
        pusher_client.trigger('alerts', str(tutor_id), {"text": f"O godzinie {lesson_time.hour}:{minute} odbędzie się lekcja {subject_changed} z {tutor_firstname} {tutor_lastname}."})

        mail_student_func = functools.partial(mail_student, student_email, student_firstname, tutor_firstname, tutor_lastname, subject_changed, lesson_time)
        mail_tutor_func = functools.partial(mail_tutor, tutor_email, tutor_firstname, student_firstname, student_lastname, subject_changed, lesson_time)

        with Pool() as pool:
            pool.map(smap, [mail_student_func, mail_tutor_func])
            print('wysłano powiadomienia o lekcjach')
    
    def return_ten_to_lesson(self):
        return self.ten_to_lesson

registry = Registry()