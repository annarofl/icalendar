from .context import TeamData

# from ical.match import Match
import pytest
import collections
from collections import OrderedDict


def _generate_team(location: str, name: str) -> OrderedDict:
    team_data = collections.OrderedDict()
    team_data['location'] = location
    team_data['name'] = name
    return team_data


class TestMatchData:
    ###########################################################################
    #  A   S A M P L E   T E A M S   S E T U P
    ###########################################################################
    @pytest.fixture(scope="class")
    def team_data(self) -> TeamData:
        data = collections.OrderedDict()
        data['me'] = 'TEAMME'
        data['start_time'] = '19:30'
        team = collections.OrderedDict()
        team['TEAM1'] = _generate_team('location 1', 'team 1')
        team['TEAMME'] = _generate_team('TeamMe Location', 'TeamMe')
        data['teams'] = team

        return TeamData(data)

    def test_team1(self, team_data):
        "Test team1 attributes"
        assert (team_data.team_name('TEAM1') == 'team 1')
        assert (team_data.team_location('TEAM1') == 'location 1')

    def test_my_team(self, team_data):
        "Test my-team attributes"
        assert (team_data.start_time() == '19:30')
        assert (team_data.my_name() == 'TeamMe')
        assert (team_data.my_location() == 'TeamMe Location')
