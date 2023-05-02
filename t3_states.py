table = {}


import json

def export_model():
    with open("model.json", "w") as outfile:
        json.dump(table, outfile)

def import_model(filename = "model.json"):
    with open(filename) as infile:
        table = json.load(infile)