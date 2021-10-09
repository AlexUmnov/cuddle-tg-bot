import json

def parse_scenarios():
    with open("scenarios.json") as scenarios_file:
        return json.load(scenarios_file)