from api.services.mail import MailService, Mail


class MailServiceMock(MailService):
    def __init__(self) -> None:
        self._mails: list[Mail] = []
    
    def send_mail(self, mail: Mail):
        self._mails.append(mail)

    def get_last_mail(self):
        return self._mails[-1]
