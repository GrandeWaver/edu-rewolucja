from pkgutil import ImpImporter
from re import sub
import sys, os
from .utils import change_last_letter, change_subject
sys.path.append(os.path.abspath('../../../'))
import secret
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
import smtplib, ssl


def mail_student(receiver_email, receiver_firstname, tutor_firstname, tutor_lastname, data, subject):

    subject_changed = change_subject(subject)

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = secret.EMAIL  # Enter your address
    password = secret.EMAIL_PASSWORD
    msg = MIMEText(f'Cześć {receiver_firstname}!\nMiło nam, że zaczynasz naukę {subject_changed} z {tutor_firstname} {tutor_lastname}! \n\nTermin pierwszej lekcji to {data.day} {data.month} o {data.hour}:00\n \nPozdrawiamy!\nZaspół korki.edu-rewolucja.pl')


    msg['Subject'] = f'Utworzyłeś zajęcia {subject_changed}'
    msg['From'] = formataddr((str(Header("korki.edu-rewolucja.pl", 'utf-8')), sender_email))
    msg['To'] = receiver_email

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Successfully sent email")
    except:
        print("Error: unable to send email")


def mail_tutor(receiver_email, receiver_firstname, student_firstname, student_lastname, data, subject):

    subject_changed = change_subject(subject)

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = secret.EMAIL  # Enter your address
    password = secret.EMAIL_PASSWORD

    a = change_last_letter(student_firstname)

    msg = MIMEText(f'Cześć {receiver_firstname}!\n{student_firstname} {student_lastname} utworzył{a} zajęcia {subject_changed}\n\nTermin pierwszej lekcji, którą poprowadzisz to {data.day} {data.month} o {data.hour}:00\n \nPozdrawiamy!\nZaspół korki.edu-rewolucja.pl')

    msg['Subject'] = f'{student_firstname} założył{a} zajęcia {subject_changed}'
    msg['From'] = formataddr((str(Header("korki.edu-rewolucja.pl", 'utf-8')), sender_email))
    msg['To'] = receiver_email

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Successfully sent email")
    except:
        print("Error: unable to send email")