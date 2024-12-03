import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailSend:
    email: str = None
    password: str = None
    server: smtplib.SMTP_SSL

    def __init__(self, email: str, password: str) -> None:
        """
        the email of the google account and the app password you generated
        """
        self.email = email
        # https://stackoverflow.com/a/27515833/16490381
        self.password = password
        self._login()

    def _login(self) -> None:
        smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtpserver.ehlo()
        smtpserver.login(self.email, self.password)
        self.server = smtpserver

    def send(self, to: list, email_text: str) -> (bool, dict):
        state = self.server.sendmail(self.email, to, email_text)
        if not state:
            return True, {}
        else:
            return False, state

    def send_html(self, to: list, subject: str, email_text: str, email_html: str) -> (bool, dict):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.email
        # msg['To'] = to

        part1 = MIMEText(email_text, 'plain')
        part2 = MIMEText(email_html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        state = self.server.sendmail(self.email, to, msg.as_string())
        if not state:
            return True, {}
        else:
            return False, state

    def __del__(self) -> None:
        print("closing connection")
        self.server.close()


class BurgerSend(GmailSend):
    def __init__(self, email: str, password: str) -> None:
        super().__init__(email, password)

    def send(self, to: list, meals: dict) -> (bool, dict):
        return super().send(to, email_text)
