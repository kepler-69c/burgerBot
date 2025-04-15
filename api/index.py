from flask import Flask, jsonify
import os
import json
import tomllib
from dotenv import load_dotenv
from helpers.fetch import Polymensa
from helpers.sendmail import BurgerSend
from helpers.datehandler import is_weekend, is_quiet_date, today

load_dotenv()
app = Flask(__name__)


#@app.route("/")
@app.route("/api")
def send_email():
    try:
        # environment variables
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        recipients = os.getenv("RECIPIENTS").split(",")

        # api config
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)
        api = config["api"]
        settings = config["settings"]

        # don't send emails on weekends / if the send variable is "never" / the date is in the quiet days list
        if settings.get("send") and settings["send"] == "never":
            return jsonify({"status": "burgerBot is disabled"}), 200
        if is_weekend():
            return jsonify({"status": "It's the weekend, no burgers today!"}), 200
        if is_quiet_date(today(), config["settings"].get("quiet_days")):
            return jsonify({"status": "today the burgerBot is quiet"}), 200

        mensa = Polymensa(**api)
        meals = mensa.get_dishes()

        # don't send emails if there is no burger and the send variable is "burger"
        if settings.get("send") and settings["send"] == "burger" and not mensa.has_burger():
            return jsonify({"status": "No burgers today!"}), 200

        mail = BurgerSend(email, password)
        mail.send(recipients, meals)

        return jsonify({"status": "Email sent successfully!", "meals": meals}), 200
    except Exception as e:
        raise e
        return jsonify({"error": str(e)}), 500


@app.route("/info")
@app.route("/api/info")
def hello():
    return "Hello, World!", 200

if __name__ == "__main__":
    app.run(debug=True)