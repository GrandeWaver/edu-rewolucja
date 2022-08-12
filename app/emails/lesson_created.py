from app.emails.main_mail import send_email
from app.emails.utils import change_last_letter, change_subject
from email.mime.text import MIMEText
from . import config


def mail_student(receiver_email, receiver_firstname, tutor_firstname, tutor_lastname, data, subject):
    subject_changed = change_subject(subject)

    msg = MIMEText(f'Cześć {receiver_firstname}!\nCieszymy się, że zaplanowałeś lekcje {subject_changed} z {tutor_firstname} {tutor_lastname}! \n\nPrzypominamy, że jej termin to {data.day} {data.month} o {data.hour}:00\n \nPozdrawiamy!\nZaspół korki.edu-rewolucja.pl')

    msg['Subject'] = f'Zaplanowałeś lekcje {subject_changed}'
    msg['From'] = config.FROM
    msg['To'] = receiver_email

    send_email(msg)


def mail_tutor(receiver_email, receiver_firstname, student_firstname, student_lastname, data, subject):
    subject_changed = change_subject(subject)
    a = change_last_letter(student_firstname)

    msg = MIMEText(f'Cześć {receiver_firstname}!\n{student_firstname} {student_lastname} właśnie zaplanował{a} z Tobą lekcje {subject_changed}!\n\nJej termin to {data.day} {data.month} o {data.hour}:00\n \nPozdrawiamy!\nZaspół korki.edu-rewolucja.pl')

    msg['Subject'] = f'{student_firstname} zaplanował{a} lekcje {subject_changed}'
    msg['From'] = config.FROM
    msg['To'] = receiver_email

    send_email(msg)