import requests
import json
import tomllib
import datetime

# settings
with open("settings.toml", "rb") as f:
    data = tomllib.load(f)
api = data["api"]

# date
today = datetime.date.today()
# if monday-friday return current day; else return next monday
if today.weekday() < 5:
    requestDay = today
    requestWeekday = today.weekday()
else:
    daysUntilMonday = 7 - today.weekday()
    requestDay = today + datetime.timedelta(days=daysUntilMonday)
    requestWeekday = 0

# request
parameters = (f"client-id={api["client_id"]}&lang={api["lang"]}"
              f"&rs-first={api["rsfirst"]}&rs-size={api["rssize"]}"
# date in format "YYYY-MM-DD". The api always return the data for the whole week, so the dates are kind of irrelevant
              f"&valid-after={requestDay}&valid-before={requestDay}&facility={api["facility"]}")
url = "https://idapps.ethz.ch/cookpit-pub-services/v1/weeklyrotas?"+parameters
response = requests.get(url)
data = response.json()

# response
meals = {}
# [0] since we're only requesting a single week, and basically all restaurants only have a single opening time
daymeals = data["weekly-rota-array"][0]["day-of-week-array"][requestWeekday]["opening-hour-array"][0]["meal-time-array"]
for arr in daymeals:
    meal = arr["name"]
    meals[meal] = []
    for dish in arr["line-array"]:
        meals[meal].append({
            "type": dish["name"],
            "name": dish["meal"]["name"],
            "description": dish["meal"]["description"],
        })


print(json.dumps(meals, indent=4, ensure_ascii=False))

# with open("data.json", "w") as f:
#     json.dump(data, f, indent=4)