"""
Created on 11 March 2020

@author: gmcwilliams
"""


class TeamData:
    """
    Manages all team data, allow query based on a team id
    """

    def __init__(self, data):
        """
        Initialise.

        """
        self.data = data

    def _lookup_value(self, team_id: str, attr: str) -> str:
        return self.data['teams'][team_id][attr]

    def start_time(self) -> str:
        return self.data['start_time']

    def my_name(self) -> str:
        return self._lookup_value(self.data['me'], 'name')

    def my_location(self) -> str:
        return self._lookup_value(self.data['me'], 'location')

    def team_name(self, team_id: str) -> str:
        return self._lookup_value(team_id, 'name')

    def team_location(self, team_id: str) -> str:
        return self._lookup_value(team_id, 'location')
