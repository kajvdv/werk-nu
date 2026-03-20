from dataclasses import dataclass
from email.message import EmailMessage
from smtplib import SMTP


@dataclass(frozen=True)
class Mail:
    from_addr: str
    to_addr: str
    subject: str
    content: str

    def to_message(self):
        msg = EmailMessage()
        msg['To'] = self.to_addr
        msg["From"] = self.from_addr
        msg['Subject'] = self.subject
        msg.set_content(self.content)
        return msg

    

class MailService:
    def send_mail(self, mail: Mail):

        with SMTP("localhost", port=1025) as smtp:
            smtp.send_message(mail.to_message())