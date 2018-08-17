"""
Created on 11 Oct 2017

@author: gmcwilliams
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from envparse import env
from icalendar import Alarm, Calendar
from icalendar.cal import Event

from .match import Match


def get_dropbox_path():
    """
    Find the default dropbox path
    """
    try:
        json_path = Path(os.getenv("LOCALAPPDATA")) / "Dropbox" / "info.json"
    except FileNotFoundError:
        json_path = Path(os.getenv("APPDATA")) / "Dropbox" / "info.json"

    with open(str(json_path)) as f:
        j = json.load(f)

    return Path(j["personal"]["path"]).absolute()


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
    # env = Env(
    #    ICAL_DATAPATH=str,
    # )
    env.read_envfile()

    dataPath = Path(env.str("ICAL_DATAPATH"), club)
    file = Path(dataPath, filename)
    if not file.exists():
        print(f"Cannot find file: {file}")
        sys.exit(1)
    return file


class Events:
    """
    Manage calendar events. Includes methods for dealing with a set of matches
    for a year.
    """

    def __init__(self, club, year):
        """
        Initialise.

        This will look for files beginning with the club name
        in the data folder. club_teams will define the shorthand for each
        opponent as well as their google maps location. club_fixtures will
        define the fixtures and date as well as recording the scores for
        matches as they are played.

        :param club: String name of the club
        :param year: String year to look for matches, e.g. 2017-18
        """

        self.savedir = get_dropbox_path()

        self.club = club
        self.year = year

        self.cal = Calendar()
        self.cal.add("prodid", "-//Bowling Calendar//mc-williams.co.uk//")
        self.cal.add("version", "2.0")
        self.cal.add("calscale", "GREGORIAN")
        self.cal.add("X-WR-TIMEZONE", "Europe/London")

        matchFile = get_match_file(club, year)
        json_matchdata = self._load_json(matchFile)
        self.duration = json_matchdata["duration"]
        self.matches = json_matchdata["matches"]

        teamFile = get_team_file(club)
        json_teamdata = self._load_json(teamFile)
        self.team_data = json_teamdata["teams"]
        self.myclub = json_teamdata["me"]

    def add_events(self):
        """Add all events for this team / season to the calendar"""

        for match in self.matches:
            match_date = match["date"]
            home_id = match["home"]
            home_score = match["home_score"]
            location = ""
            warning = ""
            if home_id in self.team_data:
                home_team_data = self.team_data[home_id]
                home_team_name = home_team_data["name"]
                location = home_team_data["location"]
            else:
                warning = "****"
                home_team_name = home_id

            away_id = match["away"]
            away_score = match["away_score"]
            if away_id in self.team_data:
                away_team_data = self.team_data[away_id]
                away_team_name = away_team_data["name"]
            else:
                warning = "****"
                away_team_name = away_id

            duration = self.duration
            if "duration" in match:
                duration = match["duration"]

            label = None
            if "label" in match:
                label = match["label"]

            new_date = None
            if "newdate" in match:
                new_date = match["newdate"]

            match = Match(
                myclub=self.myclub,
                home_team_id=home_id,
                home_team_name=home_team_name,
                home_score=home_score,
                away_team_id=away_id,
                away_team_name=away_team_name,
                away_score=away_score,
                date=match_date,
                location=location,
                warning=warning,
                duration=duration,
                label=label,
                new_date=new_date,
            )

            self.cal.add_component(self._create_event(match))
            print(match.print_description())

        # self._print_cal()
        self._write_file()

    def set_savedir(self, savedir):
        """
        Where to save the calendar. By default this is not needed and the
        default dropbox folder will be used

        :paran savedir: String path representing where to save the generated
         calendar files
        """
        self.savedir = savedir

    def _load_json(self, json_filename):
        "loads the JSON file"
        with open(json_filename) as data_file:
            json_data = json.load(data_file)
        # print(json.dumps(json_data, indent=2))
        # print(json_data['matches'])
        return json_data

    def _create_event(self, match):
        """
        Creates a calendar event for the given match

        :paran match: A Match object holding the match data
        """
        #    print(self.team_data)
        #    print(team_data)

        event = Event()
        event["uid"] = match.id()
        event["location"] = match.location
        event.add("priority", 5)

        event.add("summary", match.summary())
        event.add("description", str(match))
        event.add("dtstart", match.match_start)
        event.add("dtend", match.match_end)
        event.add("dtstamp", datetime.utcnow())

        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add("description", "Reminder")
        alarm.add("trigger", timedelta(hours=-1))
        event.add_component(alarm)

        return event

    def _mk_save_dir(self) -> Path:
        newdir = Path(self.savedir / "Apps" / "icalendar")

        if not newdir.exists():
            newdir.mkdir(parents=True)

        return newdir

    def _write_file(self):
        filename = f"{self.club}_{self.year}.ics"
        newfile = self._mk_save_dir() / filename
        newfile.write_bytes(self.cal.to_ical())
        print(f"saved:{newfile}")

    def _print_cal(self):
        print(self.cal.to_ical())
