import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
from settings import load_config


def send_mail(to_addr, url, md5_hash):
    configpath = sys.argv[2]
    email_data = load_config(configpath)['email']

    msg = MIMEMultipart()
    msg['From'] = email_data['EM_LOGIN']
    msg['To'] = to_addr
    msg['Subject'] = "MD5_Hash"

    body = "Here is the md5-hash:\n" + md5_hash + "\nand the url:\n" + url
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_data['EM_LOGIN'], email_data['EM_PASS'])
    text = msg.as_string()
    server.sendmail(email_data['EM_LOGIN'], to_addr, text)
    server.quit()
