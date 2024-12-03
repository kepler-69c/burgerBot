import smtplib


class BurgerSend(GmailSend):
    def __init__(self, email: str, password: str) -> None:
        super().__init__(email, password)

    def send(self, to: list, meals: dict) -> (bool, dict):
        return super().send(to, email_text)


class GmailSend:
    email: str = None
    password: str = None
    server: smtplib.SMTP_SSL

    def __init__(self, email: str, password: str) -> None:
        """
        the email of the google account and the app password you generated
        """
        self.email = email
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

    def __del__(self) -> None:
        print("closing connection")
        self.server.close()
