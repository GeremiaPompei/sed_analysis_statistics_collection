import smtplib
import json
from email.message import EmailMessage


class MailHandler:

    def __init__(self, credentials_path='credentials.json', thanks_and_inform_message_path='assets/mail_texts/thanks_and_inform.json'):
        credentials = json.load(open(credentials_path))
        self.smtp_host = credentials['smtp_host']
        self.smtp_port = credentials['smtp_port']
        self.smtp_user = credentials['smtp_user']
        self.smtp_password = ''
        if 'smtp_password' in credentials:
            self.smtp_password = credentials['smtp_password']
        if len(self.smtp_password) == 0:
            self.smtp_password = input('Insert "smtp_password":')
        self.thanks_and_inform_message = json.load(open(thanks_and_inform_message_path, encoding='utf-8'))

    def __call__(self, to, subject, body=''):
        s = smtplib.SMTP(self.smtp_host, self.smtp_port)
        # s.starttls()
        msg = EmailMessage()
        s.login(self.smtp_user, self.smtp_password)
        msg['from'] = self.smtp_user
        msg['to'] = to
        msg['subject'] = subject
        msg.set_content(body)
        s.send_message(msg)
        s.quit()

    def send_thanks_and_inform_message(self, user, language_id=0):
        data = self.thanks_and_inform_message[language_id]
        self(user, data['subject'].replace('[USER]', user), data['body'].replace('[USER]', user))


if __name__ == '__main__':
    mail_handler = MailHandler(credentials_path='../credentials.json')
    mail_handler(
        to="gemipampi@gmail.com",
        subject='subject',
        body="body",
    )
