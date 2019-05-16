import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime

def SendMail(img="img.jpg"):
    img_data = open(img, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Warning!!!!!!!!!!!!!!!!!!!!'
    msg['From'] = 'spycam444@gmail.com'
    msg['To'] = 'spycam444@gmail.com'
    text = MIMEText("theft detected @  "+ str(datetime.datetime.now().replace(microsecond=0)))
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(img))
    msg.attach(image)
    try:
        print("start sending....")
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        #ADD YOUR EMAIL ID AND PASSWORD AS ARGUMENT
        s.login('spycam444@gmail.com', 'sugu1234')
        s.sendmail('spycam444@gmail.com', 'spycam444@gmail.com', msg.as_string())
        print('sent sucessfully')
    except Exception:
        print('error')
    s.quit()



