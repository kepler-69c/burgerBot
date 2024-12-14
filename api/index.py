from flask import Flask, jsonify
import os
import json
import tomllib
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
        # environment variables
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        recipients = os.getenv("RECIPIENTS").split(",")

        # api config
        with open("/config.toml", "r") as f:
            config = tomllib.load(f)
        api = config["api"]

        # don't send emails on weekends or if the send variable is "never"
        if is_weekend():
            return jsonify({"status": "It's the weekend, no burgers today!"}), 200
        if api["send"] == "never":
            return jsonify({"status": "burgerBot is disabled"}), 200

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