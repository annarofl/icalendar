"""
Created on 19 Jun 2018

@author: gmcwilliams
"""
from datetime import timedelta, datetime

class Match:
    """
    Manage one match
    """

    def __init__(self, myclub, home_team_name, home_score, away_team_name, away_score, match_date, location, match_duration, label=None, new_date=None):

        self.myclub = myclub
        self.home_team_name = home_team_name
        self.home_score = home_score
        self.away_team_name = away_team_name
        self.away_score = away_score
        self.match_time = match_date
        self.location = location

        duration = timedelta(hours=match_duration)

        date_fmt_in = '%Y-%m-%d_%H:%M'
        self.match_time = datetime.strptime(self.match_time, date_fmt_in)
        # for consistency, always use the original date for id, even if match
        # time moves
        self.id_time = self.match_time.strftime('%Y-%m-%d-%H-%M')
        if (new_date is not None):
            self.match_time = datetime.strptime(new_date, date_fmt_in)
        self.match_end = self.match_time + duration
        # expect to arrive 10 mins early
        self.match_start = self.match_time - timedelta(minutes=10)

        self.label = ''
        if (label is not None):
            self.label = f" {label}"

    def summary(self):
        """Return match summary in pre-defined format"""
        summary = f'{self.home_team_name} ({self.home_score}) v ({self.away_score}) {self.away_team_name}{self.label}'
        return summary

    def description(self):
        """
        Return the match data in the defined format as a description
        """
        #display_date = self.match_start.strftime(self.date_fmt_in)
        display_date = self.match_time.strftime('%Y-%m-%d@%H:%M')
        print_description = ('%-15s (%3s) v (%3s) %-15s on %s %-31s %s' %
                             (self.home_team_name, self.home_score,
                              self.away_score, self.away_team_name,
                              display_date, self.id(), self.label))
        print(print_description)
        description = ('%s (%s) v (%s) %s on %s%s' %
                       (self.home_team_name, self.home_score,
                        self.away_score, self.away_team_name,
                        display_date, self.label))
        return description

    def id(self):
        """Define a Unique ID for the match."""

        return f'{self.myclub.replace(" ","")}-{self.id_time}@mc-williams.co.uk'
