import json
import os.path


def read_json():
    with open(os.path.join("utils", "data.json"), "r", encoding="UTF-8") as file:
        return json.load(file)






