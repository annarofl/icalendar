"""
Created on 11 March 2020

@author: gmcwilliams
"""

from .utils import get_team_data

team_data = None


def instance_for_club(club):
    global team_data
    if team_data is None:
        print("initialising team_data")
        data = get_team_data(club)
        instance_load(data.data)


def instance_load(data):
    global team_data
    if team_data is None:
        team_data = TeamData(data)


def instance():  # -> TeamData:
    global team_data
    return team_data


class TeamData:
    """
    Manages all team data, allow query based on a team id
    """

    def __init__(self, data):
        """
        Initialise.

        """
        self.data = data

    def verify_teams(self, team1_id: str, team2_id: str) -> bool:
        "true if both team_id's are valid within the data, else false"
        if team1_id in self.data['teams'] and team2_id in self.data['teams']:
            return True
        else:
            return False

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
            return team_id

    def team_location(self, team_id: str) -> str:
        """
        If the team_id is a valid team, then return the location for that team.
        Otherwise just return the passed in text.
        This allows us to add simple, random locations, e.g. in a IBA cup where
        we would not typically store the location for all the teams.
        """
        if team_id in self.data['teams']:
            return self._lookup_value(team_id, 'location')
        else:
            return team_id

    def team_start_time(self, team_id: str) -> str:
        """
        If the team has a defined start_time then use that, otherwise
        use the default league start_time
        """
        if "start_time" in self.data['teams'][team_id]:
            return self._lookup_value(team_id, 'start_time')
        else:
            return self.start_time()
