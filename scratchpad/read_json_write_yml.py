import argparse
import json
import sys
import yaml
from envparse import env
from pathlib import Path


def get_match_file(club, year):
    """
    Get the matches file for a given club/year.
    """
    return _get_file(club, f"{club}_matches_{year}.json")

def get_team_file(club):
    return _get_file(club, f"{club}_teams.json")

def _get_file(club, filename):
    """
    Get a file. The base dir will be read from env var ICAL_DATAPATH.
    If ICAL_DATAPATH is not set then the value from the .env file will be used.
    """

    dataPath = Path(env.str("ICAL_DATAPATH"), club)
    file = Path(dataPath, filename)
#    if not file.exists():
#        print(f"Cannot find file: {file}")
#        sys.exit(1)
    return file

def _load_json(json_filename):
    "loads the JSON file"
    with open(json_filename) as data_file:
        json_data = json.load(data_file)
    return json_data

parser = argparse.ArgumentParser(description="Read json bowls data, write json.")
parser.add_argument("-t", "--team")
parser.add_argument("-y", "--year")

args = parser.parse_args()

env.read_envfile()
team = args.team
year = args.year
matchFile = get_match_file(team, year)
matchdata = _load_json(matchFile)
# print(matchdata)
ymlfile = _get_file(team, f"{team}_matches_{year}.yml")
with open(ymlfile, 'w') as outfile:
    yaml.dump(matchdata, outfile, default_flow_style=False)

teamsFile = get_team_file(team)
teamdata = _load_json(teamsFile)
print(teamdata)
ymlfile = _get_file(team, f"{team}_teams.yml")
with open(ymlfile, 'w') as outfile:
    yaml.dump(teamdata, outfile, default_flow_style=False)
