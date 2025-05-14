from email.message import EmailMessage
import mimetypes
import os
import smtplib
from .update_base import UpdateBaseManager

class SendBaseEmailsManager:
    def __init__(self, emails, attachment_path, subject, body):
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
            print(f'⚠️ Arquivo não encontrado: {self.attachment_path}')
            return

        recipients = [self.to_email] + self.emails

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg, from_addr=self.smtp_user, to_addrs=recipients)
                print('✅ E-mail com anexo enviado com sucesso!')
        except Exception as e:
            print(f'❌ Erro ao enviar e-mail: {e}')

    def run(self):
        #UpdateBaseManager().run()
        self.send_email()