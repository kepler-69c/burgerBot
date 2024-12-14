import requests
import json
import datetime
from enum import Enum
from helpers.datehandler import next_weekday


class RequestState(Enum):
    LOADING = 0
    LOADED = 1
    PARSED = 2
    ERROR = 3


class Polymensa:
    requestDayStart: str = None
    requestDayEnd: str = None
    requestWeekday: str = None
    api: dict = None
    request = {
        "state": RequestState.LOADING,
        "data": None
    }
    meals: dict = {}

    def __init__(self, client_id, lang, rsfirst, rssize, facility) -> None:
        self.api = {
            "client_id": client_id,
            "lang": lang,
            "rsfirst": rsfirst,
            "rssize": rssize,
            "facility": facility
        }

        self.requestWeekday, self.requestDayStart, self.requestDayEnd = next_weekday()
        self.load_data()

    def load_data(self) -> None:
        parameters = (f"client-id={self.api['client_id']}&lang={self.api['lang']}"
                      f"&rs-first={self.api['rsfirst']
                                   }&rs-size={self.api['rssize']}"
                      # date in format "YYYY-MM-DD". The api always return the data for the whole week, so the dates are kind of irrelevant
                      f"&valid-after={self.requestDayStart}&valid-before={self.requestDayEnd}&facility={self.api['facility']}")
        url = "https://idapps.ethz.ch/cookpit-pub-services/v1/weeklyrotas?"+parameters
        response = requests.get(url)

        if response.status_code == 200:
            self.request["state"] = RequestState.LOADED
            self.request["data"] = response.json()
        else:
            self.request["state"] = RequestState.ERROR

    def parse_data(self) -> None:
        # if there was an error, exit
        if self.request["state"] == RequestState.ERROR:
            return

        # with open("dishes.json", "w") as f:
        #     f.write(json.dumps(self.request["data"]))

        # [0] since we're only requesting a single week, and basically all restaurants only have a single opening time
        daymeals = self.request["data"]["weekly-rota-array"][0]["day-of-week-array"][self.requestWeekday]["opening-hour-array"][0]["meal-time-array"]
        for arr in daymeals:
            meal = arr["name"]
            self.meals[meal] = []
            for dish in arr["line-array"]:
                self.meals[meal].append({
                    "type": dish["name"],
                    "name": dish["meal"]["name"],
                    "description": dish["meal"]["description"],
                    "image": dish["meal"].get("image-url", None),
                })

        self.request["state"] = RequestState.PARSED

    def get_dishes(self) -> dict:
        # already parsed
        if self.request["state"] == RequestState.PARSED:
            return self.meals
        # error
        elif self.request["state"] == RequestState.ERROR:
            return {"error": "error"}
        # not parsed yet
        else:
            self.parse_data()
            return self.meals

    def has_burger(self, meal: str = "Lunch") -> bool:
        if self.request["state"] == RequestState.ERROR:
            return False

        if meal not in ["Lunch", "Dinner"]:
            return False

        for m in self.meals[meal]:
            for b in ["Burger", "burger"]:
                if b in m["name"]:
                    return True

        return False
