import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from worker.celery import send_email_task
from app.settings import Settings




class MailClient:

    def __init__(self, settings: Settings):
        self.from_email = settings.from_email
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_password = settings.SMTP_PASSWORD

    @staticmethod
    def send_welcome_email(to: str) -> None:
        task_id = send_email_task.delay(f"Welcome bratku olegu", f"ay delay delay shma", to)
        return task_id


    
