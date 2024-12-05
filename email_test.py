import json
import tomllib
from helpers.fetch import Polymensa
from helpers.sendmail import BurgerSend

with open("settings.toml", "rb") as f:
    data = tomllib.load(f)
api = data["api"]

mensa = Polymensa(**api)
meals = mensa.get_dishes()

mail = BurgerSend(data["email"]["email"], data["email"]["password"])
mail.send(["sendto@gmail.com"], meals)