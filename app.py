import json
import pprint
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def ping():
    return "Hello World"


@app.route("/munros")
def munros():
    with open("munro_data.json", "r") as file:
        data = json.load(file)

    munro_property = request.args.get("property")
    if munro_property:
        filtered_data = {}
        for key, value in data.items():
            filtered_munro_data = {}
            filtered_munro_data[munro_property] = value[munro_property]
            filtered_munro_data["name"] = value["name"]
            filtered_data[key] = filtered_munro_data
        data = filtered_data

    munro_query = request.args.get("name")
    if munro_query:
        query_munros = {k: v for k, v in data.items() if munro_query in v["name"]}
        data = query_munros

    return data


@app.route("/munros/<name>")
def specific_munro(name):
    with open("munro_data.json", "r") as file:
        data = json.load(file)
        munro_object = data[name] if name in data else {}

    munro_property = request.args.get("property")
    if munro_property:
        print(munro_object[munro_property])
        return munro_object[munro_property] if munro_property in munro_object else ""
    else:
        return munro_object
