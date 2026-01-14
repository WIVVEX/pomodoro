import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from worker.celery import send_email_task
from app.settings import Settings




class MailClient:


    @staticmethod
    def send_welcome_email(to: str) -> None:
        task_id = send_email_task.delay(f"Welcome", f"first message", to)
        return task_id


    
