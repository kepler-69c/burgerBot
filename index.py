import os
import json
from helpers.fetch import Polymensa
from helpers.sendmail import BurgerSend


from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        recipients = os.getenv("RECIPIENTS").split(",")

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
        mail.send(recipients, meals)

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(meals).encode())
        return