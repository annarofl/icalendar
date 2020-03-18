"""
Created on 13 Feb 2019

@author: gmcwilliams
"""
import json
import os
import strictyaml
import sys

from envparse import env
from pathlib import Path


def savedir() -> Path:
    """
    Return a Path object for the savedir. If env ICAL_OUTPUT is set then use
    that, otherwise find the default dropbox path
    """
    if os.getenv("ICAL_OUTPUT") is not None:
        return Path(os.getenv("ICAL_OUTPUT"))

    try:
        if os.getenv("LOCALAPPDATA") is not None:
            path = Path(os.getenv("LOCALAPPDATA")) / "Dropbox" / "info.json"
        elif os.getenv("APPDATA") is not None:
            path = Path(os.getenv("APPDATA")) / "Dropbox" / "info.json"
        else:
            print("Could not find dropbox path")

        with open(str(path)) as f:
            j = json.load(f)
        return Path(j["personal"]["path"]).absolute()
    except FileNotFoundError:
        print("info.json NotFound")


def get_match_data(club, year):
    """
    Get and read the matches file for a given club/year.
    """
    filename = _get_file(club, f"{club}_matches_{year}.yml")
    return _load_data(filename)


def get_team_data(club):
    """
    Get and read the teams file for a given club.
    """
    filename = _get_file(club, f"{club}_teams.yml")
    return _load_data(filename)


def _get_file(club, filename) -> Path:
    """
    Get a file. The base dir will be read from env var ICAL_DATAPATH.
    If ICAL_DATAPATH is not set then the value from the .env file will be used.
    """
    env.read_envfile()

    dataPath = Path(env.str("ICAL_DATAPATH"), club)
    file = Path(dataPath, filename)
    if not file.exists():
        print(f"Cannot find file: {file}")
        sys.exit(1)
    return file


def _get_match_schema(self):
    return strictyaml.Map(
        {
            "duration": strictyaml.Int(),
            "matches": strictyaml.Seq(
                strictyaml.Map(
                    {
                        "away": strictyaml.Str(),
                        "date": strictyaml.Str(),
                        "newdate": strictyaml.Str(),
                        "our_score": strictyaml.Int(),
                        "opp_score": strictyaml.Int(),
                    }
                )
            ),
        }
    )


def _load_data(filename: Path, schema=None):
    "loads the data file"
    with open(filename, "r") as data_file:
        ymldata = data_file.read()
        data = strictyaml.load(ymldata, schema)
    # print(json.dumps(json_data, indent=2)) #NOSONAR
    return data
