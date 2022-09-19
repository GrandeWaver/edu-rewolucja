from . import config
from app.emails.main_mail import send_email
from email.mime.text import MIMEText

def zoom_deactivation():
    msg = MIMEText('Deauthorization Event Notification')


    msg['Subject'] = f'Zoom Deauthorization Event Notification'
    msg['From'] = config.FROM
    msg['To'] = "edurewolucja@gmail.com"

    send_email(msg)
