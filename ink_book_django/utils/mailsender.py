import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
from email.utils import make_msgid
import smtplib


class MailSender:
    def __init__(self, sender, receiver, authority_code):
        self.sender = sender
        self.authority_code = authority_code
        self.receiver = receiver

    def send_html(self, subject, content, pic_path=os.path.join(os.getcwd(), "logo.png")):
        message = MIMEMultipart('mixed')
        message.attach(MIMEText(content, "html", "utf-8"))

        message["From"] = Header(self.sender, "utf-8")
        message["To"] = Header(self.receiver, "utf-8")
        message["Subject"] = Header(subject, "utf-8")
        message['Message-ID'] = make_msgid()

        att2 = MIMEImage(open(pic_path, 'rb').read())
        att2.add_header('Content-ID', '<image1>')
        message.attach(att2)

        s = smtplib.SMTP("smtp.163.com", 25)
        try:
            s.login(self.sender, self.authority_code)
            s.sendmail(self.sender, self.receiver, message.as_string())
            print("邮件发送成功")
            return True
        except smtplib.SMTPException as e:
            print("邮件发送失败", e)
            return False
        finally:
            s.quit()

    def send_email_code(self, subject, content):
        msg = MIMEText(content)
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = self.receiver
        msg['Message-ID'] = make_msgid()

        s = smtplib.SMTP("smtp.163.com", 25)
        try:
            s.login(self.sender, self.authority_code)
            s.sendmail(self.sender, self.receiver, msg.as_string())
            print("邮件发送成功")
            return True
        except smtplib.SMTPException as e:
            print("邮件发送失败", e)
            return False
        finally:
            s.quit()


if __name__ == "__main__":
    pass