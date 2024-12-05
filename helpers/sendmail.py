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

    def __init__(self, email: str, password: str) -> None:
        super().__init__(email, password)

    def send(self, to: list, meals: dict) -> (bool, dict):
        dishes = ""
        # we're only interested in the lunch
        for dish in meals["Lunch"]:
            name = dish["name"].lower()
            if "burgers" in name or "burger" in name:
                self.has_burger = True
                self.burger = dish
            else:
                dishes += self._dish_card(dish)

        # return super().send(to, email_text)
        with open("src/template.html", "r") as f:
            html = f.read()

        body = f"""
        {self._title()}
        {self.burger_block() if self.has_burger else ""}
        {self._subtitle()}
        <div class="grid">
            {dishes}
        </div>
        """

        html = html.replace("[[email_body]]", body)
        # return html
        return super().send_html(to, "Polymensa", "", html)

    def _title(self) -> str:
        if self.has_burger:
            phrase = "Lunch plans sorted: Go get that burger!"
        else:
            phrase = "No burgers today 😿"

        html = f'<div class="title">{phrase}</div>'
        return html

    def _subtitle(self) -> str:
        if self.has_burger:
            phrase = "The other dishes are not even worth mentioning:"
        else:
            phrase = "There are some other nice dishes, though:"

        html = f'<div class="subtitle">{phrase}</div>'
        return html

    def _dish_card(self, dish: dict) -> str:
        html = f"""
        <div class="card">
            <img src="{dish["image"]}?client-id=ethz-monitor" alt="{dish["type"]}"
                class="dish-img">
            <div class="dish-container">
                <span class="heading">{dish["name"]}</span>
                <p>{dish["description"]}</p>
            </div>
        </div>
        """
        return html
    
    def burger_block(self) -> str:
        html = f"""
        <div class="burger-row">
            <img src="{self.burger["image"]}?client-id=ethz-monitor" alt="{self.burger["type"]}"
                class="burger-img">
            <div class="burger-container">
                <span class="heading">Burger</span>
                <p>{self.burger["description"]}</p>
            </div>
        </div>
        """
        return html