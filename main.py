import json
import tomllib
from helpers.fetch import Polymensa

with open("settings.toml", "rb") as f:
    data = tomllib.load(f)
api = data["api"]

mensa = Polymensa(**api)
meals = mensa.get_dishes()

print(json.dumps(meals, indent=4, ensure_ascii=False))
# print("Burgers today:", mensa.has_burger())