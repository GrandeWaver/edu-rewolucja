from . import config
from app.emails.main_mail import send_email
from app.emails.utils import change_minute, change_subject
from email.mime.text import MIMEText

def mail_student(receiver_email, receiver_firstname, tutor_firstname, tutor_lastname, subject, time):
    subject_changed = change_subject(subject)
    time.minute = change_minute(time.minute)

    msg = MIMEText(f'{receiver_firstname}, przypominamy o lekcji {subject_changed} z {tutor_firstname} {tutor_lastname}, która rozpocznie się już o {time.hour}:{time.minute} \n\nAby rozpocząć lekcje wystarczy zalogować się na korki.edu-rewolucja.pl')


    msg['Subject'] = f'Lekcja {subject_changed} z {tutor_firstname} {tutor_lastname} za 10 minut'
    msg['From'] = config.FROM
    msg['To'] = receiver_email

    send_email(msg)


def mail_tutor(receiver_email, receiver_firstname, student_firstname, student_lastname, subject, time):
    subject_changed = change_subject(subject)
    time.minute = change_minute(time.minute)

    msg = MIMEText(f'Cześć {receiver_firstname}, przypominamy o lekcji {subject_changed} z {student_firstname} {student_lastname}, która rozpocznie się już o {time.hour}:{time.minute} \n\nAby rozpocząć lekcje wystarczy zalogować się na korki.edu-rewolucja.pl\n \nPowodzenia!')

    msg['Subject'] = f'Lekcja {subject_changed} z {student_firstname} {student_lastname} za 10 minut'
    msg['From'] = config.FROM
    msg['To'] = receiver_email

    send_email(msg)