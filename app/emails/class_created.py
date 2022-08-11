from re import sub
import sys, os
sys.path.append(os.path.abspath('../../../'))
import secret
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
import smtplib, ssl


def mail_student_class_created(receiver_email, receiver_firstname, data, subject):

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
    msg = MIMEText(str('Cześć {}!\nCieszymy się, że zaplanowałeś lekcje {} dla siebie! \n\nPrzypominamy, że jej termin to {} {} o {}:00\n \nPozdrawiamy!\nZaspół {}'
    .format(receiver_firstname, subject_changed, data.day, data.month, data.hour, "korki")))


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