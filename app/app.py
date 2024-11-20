from fastapi import FastAPI
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager 
import time
from utils import *

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv 

load_dotenv()

def send_email(to_email: str,
               subject: str,
               body: str,
               is_html: bool = True):
    
    EMAIL_ID = os.getenv('EMAIL_ID')
    EMAIL_PASS = os.getenv('EMAIL_PASS')
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_ID
    msg['To'] = to_email
    msg['Subject'] = subject

    if is_html:
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ID, EMAIL_PASS)
        smtp.send_message(msg)
        smtp.quit()

def debug_cron_job():
    print("Cron Job is running...")
    
def cron_newsletter():
    print("Creating newsletter...")
    newsletter = create_newsletter()
    with open('./emails.txt', 'r') as f:
        emails = f.read().split('\n')
    
    for email in emails:
        print(f"Sending newsletter to {email}...")
        send_email(to_email=email,
                   subject='Newsletter - Athena',
                   body=newsletter)
    print("Newsletter sent...")
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(cron_newsletter, 'interval', minutes=1)
    scheduler.start()
    print("Scheduler started...")
    yield
    scheduler.shutdown()
    print("Scheduler stopped...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Status": "Running..."}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host='0.0.0.0', port=1414)