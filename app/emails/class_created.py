from app.emails.main_mail import send_email
from .utils import change_last_letter, change_subject
from email.mime.text import MIMEText
from . import config


def mail_student(receiver_email, receiver_firstname, tutor_firstname, tutor_lastname, data, subject):
    subject_changed = change_subject(subject)

    msg = MIMEText(f'Cześć {receiver_firstname}!\nMiło nam, że zaczynasz naukę {subject_changed} z {tutor_firstname} {tutor_lastname}! \n\nTermin pierwszej lekcji to {data.day} {data.month} o {data.hour}:00\n \nPozdrawiamy!\nZaspół korki.edu-rewolucja.pl')


    msg['Subject'] = f'Utworzyłeś zajęcia {subject_changed}'
    msg['From'] = config.FROM
    msg['To'] = receiver_email

    send_email(msg)


def mail_tutor(receiver_email, receiver_firstname, student_firstname, student_lastname, data, subject):
    subject_changed = change_subject(subject)
    a = change_last_letter(student_firstname)

    msg = MIMEText(f'Cześć {receiver_firstname}!\n{student_firstname} {student_lastname} utworzył{a} zajęcia {subject_changed}\n\nTermin pierwszej lekcji, którą poprowadzisz to {data.day} {data.month} o {data.hour}:00\n \nPozdrawiamy!\nZaspół korki.edu-rewolucja.pl')

    msg['Subject'] = f'{student_firstname} założył{a} zajęcia {subject_changed}'
    msg['From'] = config.FROM
    msg['To'] = receiver_email

    send_email(msg)