"""
Created on 11 March 2020

@author: gmcwilliams
"""

from ical.utils import get_team_data


def instance(club):  # -> TeamData:
    data = get_team_data(club)
    return TeamData(data.data)


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

    def my_id(self) -> str:
        return self.data['me']

    def my_name(self) -> str:
        return self._lookup_value(self.data['me'], 'name')

    def my_location(self) -> str:
        return self._lookup_value(self.data['me'], 'location')

    def team_name(self, team_id: str) -> str:
        if team_id in self.data['teams']:
            return self._lookup_value(team_id, 'name')
        else:
            return f"**** {team_id}"

    def team_location(self, team_id: str) -> str:
        return self._lookup_value(team_id, 'location')

    def team_start_time(self, team_id: str) -> str:
        """
        If the team has a defined start_time then use that, otherwise
        use the default league start_time
        """
        if "start_time" in self.data['teams'][team_id]:
            return self._lookup_value(team_id, 'start_time')
        else:
            return self.start_time()
