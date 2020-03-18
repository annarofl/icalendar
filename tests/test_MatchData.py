from .context import TeamData

# from ical.match import Match
import pytest
import collections
from collections import OrderedDict


def _generate_team(location: str, name: str, start_time: str = None) -> OrderedDict:
    team_data = collections.OrderedDict()
    team_data['location'] = location
    team_data['name'] = name
    if start_time is not None:
        team_data['start_time'] = start_time
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
        team['TEAM2'] = _generate_team('location 2', 'team 2', '20:00')
        team['TEAMME'] = _generate_team('TeamMe Location', 'TeamMe')
        data['teams'] = team

        return TeamData(data)

    def test_team1(self, team_data):
        "Test team1 attributes"
        assert (team_data.team_name('TEAM1') == 'team 1')
        assert (team_data.team_location('TEAM1') == 'location 1')
        assert (team_data.team_start_time('TEAM1') == '19:30')

    def test_team2(self, team_data):
        "Test team2 attributes"
        assert (team_data.team_name('TEAM2') == 'team 2')
        assert (team_data.team_location('TEAM2') == 'location 2')

    def test_team_invalid(self, team_data):
        "Test team id missing from data"
        id = 'XYZZY'
        assert (team_data.team_name(id) == f'**** {id}')

    def test_my_team(self, team_data):
        "Test my-team attributes"
        assert (team_data.start_time() == '19:30')
        assert (team_data.my_name() == 'TeamMe')
        assert (team_data.my_location() == 'TeamMe Location')
