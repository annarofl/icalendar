"""
Created on 11 Oct 2017

@author: gmcwilliams
"""
from .utils import savedir, get_match_data
from .match import Match
from datetime import datetime, timedelta
from pathlib import Path

from icalendar import Alarm, Calendar
from icalendar.cal import Event
from ical import teamdata


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

        matchdata = get_match_data(club, year)
        self.duration = float(matchdata["duration"])
        self.matches = matchdata["matches"]

        self.team_data = teamdata.instance()
        self.default_start_time = self.team_data.start_time()

    def add_events(self):
        """Add all events for this team / season to the calendar"""

        for match in self.matches:
            self._process_match(match)

        self._write_file()

    def _process_match(self, match):
            match_date = match["date"]
            # match will be defined as "home": "Opponent" meaning WE are HOME
            # against the Opponent, so some of the following will appear to be
            # processed back to front (or home to away)

            self._setup_home_and_away(match)

            location = ""

            location = self.team_data.team_location(self.home_id)
            start_time = self.team_data.team_start_time(self.home_id)

            if "location" in match: #  match location can be a link to another club, e.g. neutral venue
                location = self.team_data.team_location(match["location"])

            if "start_time" in match: #  allow specification of new start time, e.g. Playing outdoor at venue
                                      #  where match usually starts at 2:200, but cup starts at 5:00
                start_time = match["start_time"]

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
                home_team_id=self.home_id,
                home_score=self.home_score.data,
                away_team_id=self.away_id,
                away_score=self.away_score.data,
                date=match_date,
                time=start_time,
                location=location,
                duration=duration,
                label=label,
                new_date=new_date,
            )

            # 32: If new_date is "" then don't add event, but still print
            # match content
            if new_date != "":
                self.cal.add_component(self._create_event(match))

            print(match.print_description())

    def _setup_home_and_away(self, match):
        if "home" in match:
            self.home_id = self.team_data.my_id()
            self.home_score = match["our_score"]
            self.away_id = match["home"].data
            self.away_score = match["opp_score"]
        else:
            self.home_id = match["away"].data
            self.home_score = match["opp_score"]
            self.away_id = self.team_data.my_id()
            self.away_score = match["our_score"]

    def set_savedir(self, savedir):
        """
        Where to save the calendar. By default this is not needed and the
        default dropbox folder will be used

        :paran savedir: String path representing where to save the generated
         calendar files
        """
        self.savedir = savedir

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
