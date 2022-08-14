import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os

sender_email = {'name': 'Jen', 'addr': os.environ.get("SENDER_ADDR")}
receiver_email = os.environ.get("RECEIVER_ADDR") 
password = os.environ.get("PASSWORD") 

msg = MIMEMultipart()
msg['From'] = sender_email['name']
msg['To'] = receiver_email
msg['Subject'] = Header("自動提醒", 'utf-8').encode()

html = f"""\
<html>
  <body>
    <p>你好,<br>
       請記得繳{os.environ.get("BANK")}帳單!!!<br>
    </p>
  </body>
</html>
"""

msg_content = MIMEText(html, 'html')
msg.attach(msg_content)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server: #指定SMTP伺服器的位置以及它的通訊埠
    server.login(sender_email['addr'], password) #登入SMTP伺服器
    status = server.sendmail(sender_email['addr'], receiver_email, msg.as_string()) #傳送電子郵件訊息
    
    if not bool(status): #bool可省略, status有「錯誤」時會回傳true
        print('Success')
    else:
        print(f'Failure。 {status}')