from helpers.sendmail import GmailSend
import tomllib

with open("settings.toml", "rb") as f:
    data = tomllib.load(f)
email = data["email"]

mail = GmailSend(email["email"], email["password"])

text = "This is your polymensa menu for the day:\n\nBreakfast: {}\nLunch: {}\nDinner: {}".format("hj", "hj", "hjk")
with open("src/email.html", "r") as f:
    html = f.read()

mail.send_html(["planet.kepler.69c@gmail.com"], "test", text, html)

mail.send(["planet.kepler.69c@gmail.com"], "test")
mail.send(["planet.kepler.69c@gmail.com"], "test")