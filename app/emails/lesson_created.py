from pkgutil import ImpImporter
from re import sub
import sys, os
sys.path.append(os.path.abspath('../../../'))
import secret
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
import smtplib, ssl


def mail_student(receiver_email, receiver_firstname, tutor_firstname, tutor_lastname, data, subject):

    if subject == 'matematyka':
        subject_changed = 'matematyki'
    elif subject == 'angielski':
        subject_changed = 'angielskiego'
    else:
        subject_changed = subject

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = secret.EMAIL  # Enter your address
    password = secret.EMAIL_PASSWORD
    msg = MIMEText(f'Cześć {receiver_firstname}!\nCieszymy się, że zaplanowałeś lekcje {subject_changed} z {tutor_firstname} {tutor_lastname}! \n\nPrzypominamy, że jej termin to {data.day} {data.month} o {data.hour}:00\n \nPozdrawiamy!\nZaspół korki.edu-rewolucja.pl')


    msg['Subject'] = f'Zaplanowałeś lekcje {subject_changed}'
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

    if subject == 'matematyka':
        subject_changed = 'matematyki'
    elif subject == 'angielski':
        subject_changed = 'angielskiego'
    else:
        subject_changed = subject

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = secret.EMAIL  # Enter your address
    password = secret.EMAIL_PASSWORD

    if student_lastname[-1] == 'a':
        a = 'a'
    else:
        a = ''

    msg = MIMEText(f'Cześć {receiver_firstname}!\n{student_firstname} {student_lastname} właśnie zaplanował{a} z tobą lekcje {subject_changed}!\n\nJej termin to {data.day} {data.month} o {data.hour}:00\n \nPozdrawiamy!\nZaspół korki.edu-rewolucja.pl')

    msg['Subject'] = f'{student_firstname} zaplanował{a} lekcje {subject_changed}'
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