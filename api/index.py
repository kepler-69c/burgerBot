from flask import Flask, jsonify
import os
import json
import datetime
from dotenv import load_dotenv
from helpers.fetch import Polymensa
from helpers.sendmail import BurgerSend
from helpers.datehandler import is_weekend

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
            "client_id": "ethz-wcms",  # TODO: am I allowed to use this id?
            # language; possible: ["en", "de"]
            "lang": "en",
            # idk, since the API always returns the same number of records
            "rsfirst": 0,
            "rssize": 1,
            # facility number
            "facility": 9,
        }

        # don't send emails on weekends
        if is_weekend():
            return jsonify({"status": "It's the weekend, no burgers today!"}), 200

        mensa = Polymensa(**api)
        meals = mensa.get_dishes()

        mail = BurgerSend(email, password)
        mail.send(recipients, meals)

        return jsonify({"status": "Email sent successfully!", "meals": meals}), 200
    except Exception as e:
        raise e
        return jsonify({"error": str(e)}), 500


@app.route("/hello")
@app.route("/api/hello")
def hello():
    return "Hello, World!", 200

if __name__ == "__main__":
    app.run(debug=True)