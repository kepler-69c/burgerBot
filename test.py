from helpers.sendmail import GmailSend
import tomllib

with open("settings.toml", "rb") as f:
    data = tomllib.load(f)
email = data["email"]

mail = GmailSend(email["email"], email["password"])
mail.send(["mail@example.com"], "test")