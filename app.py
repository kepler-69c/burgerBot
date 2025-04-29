from flask import Flask, jsonify, render_template
import os
import json
import tomllib
from dotenv import load_dotenv

from helpers.db import get_emails, update_settings, get_email
from helpers.fetch import Polymensa
from helpers.sendmail import BurgerSend
from helpers.datehandler import is_weekend, is_quiet_date, today

load_dotenv()
app = Flask(__name__)


@app.route("/api")
def send_email():
    try:
        # environment variables
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")

        # config.toml variables
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)
        env = config["env"]
        api = config["api"]
        settings = config["settings"]

        # don't send emails on weekends / the date is in the quiet days list
        if is_quiet_date(today(), settings.get("quiet")):
            return jsonify({"status": "today the burgerBot is quiet"}), 200
        if is_weekend():
            return jsonify({"status": "It's the weekend, no burgers today!"}), 200

        # get data from polymensa, recipients from database
        mensa = Polymensa(**api)
        meals = mensa.get_dishes()
        recipients = get_emails()
        sent = 0

        # send email to every recipient, adhering to the settings and enviroment
        mail = BurgerSend(email, password, meals, settings.get("url"))
        for token, re in recipients.items():
            # skip if dev environment
            if env == "dev" and not re.get("development"):
                print(f"skipping prod recipient { re.get("email") }")
                continue
            # skip if settings is "never" or "burger" and there is no burger
            sending = re.get("sending")
            if sending == "never" or sending == "burger" and not mensa.has_burger():
                print(f"skipping recipient { re.get("email") } because of settings")
                continue
            # send email
            mail.send(token, re)
            sent += 1

        return jsonify({"status": f"Email sent successfully to {sent} recipients!", "meals": meals}), 200
    except Exception as e:
        raise e
        return jsonify({"error": str(e)}), 500


@app.route("/")
def hello():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    return render_template("index.html", config=config)


@app.route("/api/change/<token>/<sending>", methods=["GET", "POST"])
def change_settings(token, sending):
    data = get_email(token)
    if data and sending in ["always", "never", "burger"]:
        update_settings(token, sending)
        return render_template("settings.html", found=True, email=data["email"], setting=sending, token=token), 200
    else:
        return render_template("settings.html", found=False, token=token), 400