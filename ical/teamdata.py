"""
Created on 11 Oct 2017

@author: gmcwilliams
"""
#from .utils import savedir, get_team_data, get_match_data
#from .match import Match
#from datetime import datetime, timedelta
#from pathlib import Path

#from icalendar import Alarm, Calendar
#from icalendar.cal import Event


class TeamData:
    """
    Manages all team data, allow query based on a team id
    """

    def __init__(self, data):
        """
        Initialise.

        """
#        print(f"data={data}")
#        for k, v in data.items():
#            print(f"k={k}, v={v}")

        self.data = data

    def _lookup_value(self, teamId: str, attr: str) -> str:
        return self.data['teams'][teamId][attr]

    def start_time(self) -> str:
        return self.data['start_time']

    def my_name(self) -> str:
        return self._lookup_value(self.data['me'], 'name')

    def my_location(self) -> str:
        return self._lookup_value(self.data['me'], 'location')

    def team_name(self, teamId: str) -> str:
        return self._lookup_value(teamId, 'name')

    def team_location(self, teamId: str) -> str:
        return self._lookup_value(teamId, 'location')
