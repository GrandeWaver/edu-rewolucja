import sys, os
sys.path.append(os.path.abspath('../../../'))
import secret
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
import smtplib, ssl


def mail_lesson_created(receiver_email, receiver_firstname, data):
    print(secret.EMAIL)
    print(secret.EMAIL_PASSWORD)
    print(receiver_email)
    print(data)

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = secret.EMAIL  # Enter your address
    password = secret.EMAIL_PASSWORD
    msg = MIMEText(str('Cześć {}!\nCieszymy się, że zaplanowałeś lekcje dla siebie! \n\nPrzypominamy, że jej termin to {} {} o {}:00\n \nPozdrawiamy!\nZaspół {}'
    .format(receiver_firstname, data.day, data.month, data.hour, "korki")))

    msg['Subject'] = "Zaplanowałeś lekcje"
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