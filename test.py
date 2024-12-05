import os
import tomllib
from helpers.sendmail import GmailSend

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
recipients = os.getenv("RECIPIENTS").split(",")

mail = GmailSend(email, password)

text = "This is your polymensa menu for the day:\n\nBreakfast: {}\nLunch: {}\nDinner: {}".format(
    "hj", "hj", "hjk")
with open("src/email.html", "r") as f:
    html = f.read()

mail.send_html(recipients, "test", text, html)
