"""
Created on 11 Oct 2017

@author: gmcwilliams
"""
import json
import os
import strictyaml
import sys
from datetime import datetime, timedelta
from pathlib import Path

from envparse import env
from icalendar import Alarm, Calendar
from icalendar.cal import Event

from .match import Match


def savedir():
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


def get_match_file(club, year):
    """
    Get the matches file for a given club/year.
    """
    return _get_file(club, f"{club}_matches_{year}.yml")


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


def get_team_file(club):
    return _get_file(club, f"{club}_teams.yml")


def _get_file(club, filename):
    """
    Get a file. The base dir will be read from env var ICAL_DATAPATH.
    If ICAL_DATAPATH is not set then the value from the .env file will be used.
    """
    # env = Env(
    #    ICAL_DATAPATH=str,
    # )
    env.read_envfile()

    print(env.str("ICAL_DATAPATH"))
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

        self.savedir = savedir()

        self.club = club
        self.year = year

        self.cal = Calendar()
        self.cal.add("prodid", "-//Bowling Calendar//mc-williams.co.uk//")
        self.cal.add("version", "2.0")
        self.cal.add("calscale", "GREGORIAN")
        self.cal.add("X-WR-TIMEZONE", "Europe/London")

        matchFile = get_match_file(club, year)
        matchdata = self._load_data(matchFile)
        self.duration = float(matchdata["duration"])
        self.matches = matchdata["matches"]

        teamFile = get_team_file(club)
        teamdata = self._load_data(teamFile, None)
        self.team_data = teamdata["teams"]
        self.myclub = teamdata["me"]
        self.default_start_time = teamdata["start_time"]

    def add_events(self):
        """Add all events for this team / season to the calendar"""

        for match in self.matches:
            match_date = match["date"]
            # match will be defined as "home": "Opponent" meaning WE are HOME
            # against the Opponent, so some of the following will appear to be processed
            # back to front (or home to away)
            if "home" in match:
                home_id = self.myclub
                home_score = match["our_score"]
                away_id = match["home"]
                away_score = match["opp_score"]
            else:
                home_id = match["away"]
                home_score = match["opp_score"]
                away_id = self.myclub
                away_score = match["our_score"]

            location = ""
            warning = ""
            start_time = self.default_start_time

            if home_id in self.team_data:
                home_team_data = self.team_data[home_id]
                home_team_name = home_team_data["name"]
                location = home_team_data["location"]
                if "start_time" in home_team_data:
                    start_time = home_team_data["start_time"]
            else:
                warning = "****"
                home_team_name = home_id

            if "start_time" in match:
                start_time = match["start_time"]

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
                myclub=self.myclub.data,
                home_team_id=home_id.data,
                home_team_name=home_team_name.data,
                home_score=home_score.data,
                away_team_id=away_id.data,
                away_team_name=away_team_name.data,
                away_score=away_score.data,
                date=match_date,
                time=start_time,
                location=location,
                warning=warning,
                duration=duration,
                label=label,
                new_date=new_date,
            )

            # 32: If new_date is "" then don't add event, but still print match content
            if new_date != "":
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

    def _load_data(self, filename: str, schema=None):
        "loads the data file"
        with open(filename, "r") as data_file:
            ymldata = data_file.read()
            data = strictyaml.load(ymldata, schema)
        # print(json.dumps(json_data, indent=2))
        # print(json_data['matches'])
        return data

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