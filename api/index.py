from flask import Flask, jsonify
import os
import json
from dotenv import load_dotenv
from helpers.fetch import Polymensa
from helpers.sendmail import BurgerSend

load_dotenv()
app = Flask(__name__)


@app.route("/")
@app.route("/api")
def send_email():
    try:
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        recipients = os.getenv("RECIPIENTS").split(",")

        api = {
            # id which indicates which eth service is requesting the data
            client_id: "ethz-wcms",  # TODO: am I allowed to use this id?
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

        return jsonify({"status": "Email sent successfully!", "meals": meals}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
