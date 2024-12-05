import os
import json
from helpers.fetch import Polymensa
from helpers.sendmail import BurgerSend

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

api = {
    # id which indicates which eth service is requesting the data
    client_id: "ethz-wcms", # TODO: am I allowed to use this id?
    # language; possible: ["en", "de"]
    lang: "en",
    # idk
    rsfirst: 0,
    rssize: 1,
    # facility number
    facility: 9,
}

mensa = Polymensa(**api)
meals = mensa.get_dishes()

mail = BurgerSend(email, password)
mail.send(["sendto@gmail.com"], meals)