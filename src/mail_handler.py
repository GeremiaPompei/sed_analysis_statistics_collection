import smtplib
import json


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
        self.thanks_and_inform_message = json.load(open(thanks_and_inform_message_path))

    def __call__(self, to, subject, body=''):
        message = 'Subject: {}\n\n{}'.format(subject, body)
        s = smtplib.SMTP(self.smtp_host, self.smtp_port)
        # s.starttls()
        s.login(self.smtp_user, self.smtp_password)
        s.sendmail(self.smtp_user, to, message)
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
