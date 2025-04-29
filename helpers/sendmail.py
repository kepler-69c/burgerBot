import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Tuple


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

    def send(self, to: list, email_text: str) -> Tuple[bool, dict]:
        state = self.server.sendmail(self.email, to, email_text)
        if not state:
            return True, {}
        else:
            return False, state

    def send_html(self, to: list, subject: str, email_text: str, email_html: str) -> Tuple[bool, dict]:
        # https://stackoverflow.com/a/882770/16490381
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.email

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
    has_burger: bool = False
    burger: dict = None
    meals: dict = None
    current_url: str = None

    def __init__(self, email: str, password: str, meals: dict, current_url: str = None) -> None:
        super().__init__(email, password)
        self.meals = meals
        self.current_url = current_url

    def send(self, token: str, recipient: dict) -> Tuple[bool, dict]:
        dishes = ""
        # we're only interested in the lunch
        for dish in self.meals["Lunch"]:
            name = dish["name"].lower()
            if "burgers" in name or "burger" in name:
                self.has_burger = True
                self.burger = dish
            else:
                dishes += self._dish_card(dish)

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head></head>
        <body>
            <h1>{self._title()}</h1>
            {self._burger_block() if self.has_burger else ""}
            <h2>{self._subtitle()}</h2>
            <ul>
                {dishes}
            </ul>
            <p>
                <small>
                    change notifications to
                    <a href="{self.current_url}/api/change/{token}/always">always</a> - 
                    <a href="{self.current_url}/api/change/{token}/never">never</a> - 
                    <a href="{self.current_url}/api/change/{token}/burger">burger only</a>
                </small>
            </p>
        </body>
        </html>
        """
        # return html
        return super().send_html([recipient["email"]], "Polymensa", "", html)

    def _title(self) -> str:
        if self.has_burger:
            return "Lunch plans sorted: Go get that burger!"
        else:
            return "No burgers today 😿"

    def _subtitle(self) -> str:
        if self.has_burger:
            return "The other dishes are not even worth mentioning:"
        else:
            return "There are some other nice dishes, though:"

    def _dish_card(self, dish: dict) -> str:
        html = f"""
        <li><p><strong>{dish["name"]}</strong><br>{dish["description"]}</p></li>
        """
        return html

    def _burger_block(self) -> str:
        html = f"""
        <p><strong>{self.burger["name"]}</strong><br>{self.burger["description"]}</p>
        """
        return html
