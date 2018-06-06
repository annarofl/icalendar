"""
Created on 11 Oct 2017

@author: gmcwilliams
"""
from icalendar import Calendar, Alarm
import json
from datetime import timedelta, datetime
from icalendar.cal import Event
import os
from pathlib import Path


def get_dropbox_path():
    """
    Find the default dropbox path
    """
    try:
        json_path = Path(os.getenv('LOCALAPPDATA')) / 'Dropbox' / 'info.json'
    except FileNotFoundError:
        json_path = Path(os.getenv('APPDATA')) / 'Dropbox' / 'info.json'

    with open(str(json_path)) as f:
        j = json.load(f)

    return Path(j['personal']['path']).resolve().absolute()


class Events:
    """
    Manage calendar events. Includes methods for dealing with a set of matches for a
    year.
    """

    def __init__(self, club, year):
        """
        Initialise.

        This will look for files beginning with the club name
        in the data folder. club_teams will define the shorthand for each
        opponent as well as their google maps location. club_fixtures will
        define the fixtures and date as well as recording the scores for matches
        as they are played.

        :param club: String name of the club
        :param year: String year to look for matches, e.g. 2017-18
        """

        self.savedir = get_dropbox_path()

        self.club = club
        self.year = year

        self.cal = Calendar()
        self.cal.add('prodid', '-//Bowling Calendar//mc-williams.co.uk//')
        self.cal.add('version', '2.0')
        self.cal.add('calscale', 'GREGORIAN')
        self.cal.add('X-WR-TIMEZONE', 'Europe/London')

        dataPath = Path('data', club)
        matchFile = Path(dataPath, f'{club}_matches_{year}.json')

        json_matchdata = self._load_json(matchFile)
        self.duration = json_matchdata['duration']
        self.matches = json_matchdata['matches']

        teamFile = Path(dataPath, f'{club}_teams.json')
        json_teamdata = self._load_json(teamFile)
        self.team_data = json_teamdata['teams']
        self.myclub = json_teamdata['me']

    def add_events(self):
        """Add all events for this team / season to the calendar"""

        for match in self.matches:
            match = Match(match, self.team_data, self.myclub,
                          self.year, self.duration)
            self.cal.add_component(self._create_event(match))

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
    #    print(match_data)
    #    print(team_data)

        event = Event()
        event['uid'] = match.id()
        event['location'] = match.location
        event.add('priority', 5)

        event.add('summary', match.summary())
        event.add('description', match.description())
        event.add('dtstart', match.match_start)
        event.add('dtend', match.match_end)
        event.add('dtstamp', datetime.utcnow())

        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add('description', "Reminder")
        alarm.add("trigger", timedelta(hours=-1))
        event.add_component(alarm)

        match.print_description()

        return event

    def _mk_save_dir(self):
        newdir = Path(self.savedir) / 'Apps' / 'icalendar'

        if not newdir.exists():
            newdir.mkdir(parents=True)

        return newdir

    def _write_file(self):
        filename = f'{self.club}_{self.year}.ics'
        newfile = self._mk_save_dir() / filename
        newfile.write_bytes(self.cal.to_ical())
        print(f'saved:{newfile}')

    def _print_cal(self):
        print(self.cal.to_ical())


class Match:
    """
    Manage one match
    """

    def __init__(self, match_data, team_data, myclub, year, match_duration):

        self.team_data = team_data
        self.myclub = myclub
        self.year = year

        self.home_id = match_data['home']
        self.warning = ""
        if self.home_id in self.team_data:
            home_team_data = self.team_data[self.home_id]
            self.home_team_name = home_team_data['name']
            self.location = home_team_data['location']
        else:
            self.warning = "****"
            self.home_team_name = self.home_id
            self.location = ""

        self.home_score = match_data['home_score']

        self.away_id = match_data['away']
        if self.away_id in self.team_data:
            away_team_data = self.team_data[self.away_id]
            self.away_team_name = away_team_data['name']
        else:
            self.warning = "****"
            self.away_team_name = self.away_id
        self.away_score = match_data['away_score']

        duration = timedelta(hours=match_duration)
        if 'duration' in match_data:
            duration = timedelta(hours=match_data['duration'])
        elif 'duration_minutes' in match_data:
            duration = timedelta(minutes=match_data['duration_minutes'])

        date_fmt_in = '%Y-%m-%d_%H:%M'
        self.match_time = datetime.strptime(match_data['date'], date_fmt_in)
        # for consistency, always use the original date for id, even if match
        # time moves
        self.id_time = self.match_time.strftime('%Y-%m-%d-%H-%M')
        if ('newdate' in match_data):
            self.match_time = datetime.strptime(
                match_data['newdate'], date_fmt_in)
        self.display_date = self.match_time.strftime('%Y-%m-%d@%H:%M')
        self.match_end = self.match_time + duration
        # expect to arrive 10 mins early
        self.match_start = self.match_time - timedelta(minutes=10)

        self.label = ''
        if ('label' in match_data):
            self.label = f" {match_data['label']}"

    def summary(self):
        """Return match summary in pre-defined format"""
        summary = f'{self.home_team_name} ({self.home_score}) v ({self.away_score}) {self.away_team_name}{self.label}'
        return summary

    def description(self):
        """
        Return the match data in the defined format as a description
        """
        description = f'{self.home_team_name} ({self.home_score}) v ({self.away_score}) {self.away_team_name} on {self.display_date} {self.label}'
        return description

    def print_description(self):
        """
        Print a description of the match
        """
        print_description = ('%-15s (%3s) v (%3s) %-15s on %s %-31s %s %s' %
                             (self.home_team_name, self.home_score,
                              self.away_score, self.away_team_name,
                              self.display_date, self.id(), self.label, self.warning))
        print(print_description)

    def id(self):
        """Define a Unique ID for the match."""

        # if we move match times, e.g. a cup game, then we cannot use simply the time,
        # otherwise bot the original and the new game will have same ID, so need to add
        # the clubname
        id_team = self.home_id
        if self.home_id == self.myclub:
            id_team = self.away_id
        id_team = id_team.replace(" ","")
        return f'{self.myclub.replace(" ","")}-{self.id_time}-{id_team}@mc-williams.co.uk'
