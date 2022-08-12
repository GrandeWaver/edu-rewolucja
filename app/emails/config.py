from email.header import Header
from email.utils import formataddr
import sys, os
sys.path.append(os.path.abspath('../../../'))
import secret

PORT = 465  # For SSL
SMTP_SERVER = "smtp.gmail.com"
FROM = formataddr((str(Header("korki.edu-rewolucja.pl", 'utf-8')), secret.EMAIL))