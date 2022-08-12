import sys, os
sys.path.append(os.path.abspath('../../../'))
import secret
import smtplib, ssl
from . import config

def send_email(msg):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.PORT, context=context) as server:
            server.login(secret.EMAIL, secret.EMAIL_PASSWORD)
            server.sendmail(secret.EMAIL, msg['To'], msg.as_string())
            print("Successfully sent email")
    except:
        print("Error: unable to send email")