import smtplib
from email.mime.text import MIMEText

def send_email_code(to_email: str, code: str):
    my_account="15088797151@163.com"
    my_password="NAhnECXzuQiQeG87"
    msg = MIMEText(f"你的验证码是：{code}，5分钟内有效。")
    msg['Subject'] = '注册验证码'
    msg['From'] = my_account
    msg['To'] = to_email

    with smtplib.SMTP_SSL("smtp.163.com", 465) as server:
        server.login(my_account,my_password)
        server.send_message(msg)
