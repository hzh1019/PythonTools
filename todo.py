import pandas as pd
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(to, subject, body, file=None):
    sender_email = "example@gmail.com"
    sender_password = "password"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, "plain"))
    if file:
        with open(file, "rb") as f:
            attach = MIMEApplication(f.read(),_subtype="xlsx")
            attach.add_header('Content-Disposition','attachment',filename=str(file))
            msg.attach(attach)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, to, text)
    server.quit()

def job():
    df = pd.read_excel("todo_list.xlsx")
    for index, row in df.iterrows():
        if pd.Timestamp.now().date() == row['Due Date'].date():
            send_email(row['Email'], row['Task'], row['Description'], row['Attachment'])

schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
