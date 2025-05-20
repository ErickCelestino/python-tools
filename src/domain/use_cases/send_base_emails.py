import mimetypes
import os
import smtplib
import pythoncom
from .update_base import UpdateBaseManager
from email.message import EmailMessage

class SendBaseEmailsManager:
    def __init__(self, emails, attachment_path, subject, body, notify_callback=None):
        # Outlook Settings (Microsoft 365)
        self.smtp_server = 'smtp.office365.com'
        self.smtp_port = 587
        self.smtp_user = os.getenv("USER_EMAIL")
        self.smtp_password = os.getenv("PASSWORD_EMAIL")

        # Email data
        self.to_email = 'vp.financas@vitru.com.br'
        self.emails = emails
        self.subject = subject
        self.body = body

        self.attachment_path = attachment_path

        self.notify_callback = notify_callback or (lambda msg, bgcolor='': None)

    def notify(self, message: str, bgcolor='green', text_color='white'):
        self.notify_callback(message, bgcolor, text_color)

    def send_email(self):
        msg = EmailMessage()
        msg['Subject'] = self.subject
        msg['From'] = self.smtp_user
        msg['To'] = self.to_email
        msg['Cc'] = ', '.join(self.emails)
        msg.set_content(self.body)

        if os.path.exists(self.attachment_path):
            file_name = os.path.basename(self.attachment_path)
            mime_type, _ = mimetypes.guess_type(self.attachment_path)
            mime_type = mime_type or 'application/octet-stream'
            main_type, sub_type = mime_type.split('/', 1)

            with open(self.attachment_path, 'rb') as f:
                msg.add_attachment(f.read(),
                                   maintype=main_type,
                                   subtype=sub_type,
                                   filename=file_name)
        else:
            warning_message = f'⚠️ Arquivo não encontrado: {self.attachment_path}'
            print(warning_message)
            self.notify(msg, bgcolor='yellow', text_color='black')
            return

        recipients = [self.to_email] + self.emails

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg, from_addr=self.smtp_user, to_addrs=recipients)
                sucess_message = '✅ E-mail com anexo enviado com sucesso!'
                print(sucess_message)
                self.notify(sucess_message, bgcolor='green')
        except Exception as e:
            error_msg = f'❌ Erro ao enviar e-mail: {e}'
            print(error_msg)
            self.notify(error_msg, bgcolor='red')

    def run(self):
        pythoncom.CoInitialize()
        try:
            UpdateBaseManager().run()
            self.send_email()
        finally:
            pythoncom.CoUninitialize()