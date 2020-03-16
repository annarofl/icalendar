from .context import TeamData

# from ical.match import Match
import pytest
import collections


def _generate_team(location: str, name: str):
    team_data = collections.OrderedDict()
    team_data['location'] = location
    team_data['name'] = name
    return team_data


class TestMatchData:
    ###########################################################################
    #  H O M E
    ###########################################################################
    @pytest.fixture(scope="class")
    def team_data(self) -> TeamData:
        data = collections.OrderedDict()
        data['me'] = 'FALLSIA'
        data['start_time'] = '19:30'
        team = collections.OrderedDict()
        team['TEAM1'] = _generate_team('location 1', 'team 1')
        team['FALLSIA'] = _generate_team('FallsIA Location', 'FallsIA')
        data['teams'] = team

        return TeamData(data)

    def test_one(self, team_data):
        assert (team_data.start_time() == '19:30')
        assert (team_data.team_name('TEAM1') == 'team 1')

    def test_me(self, team_data):
        assert (team_data.start_time() == '19:30')
        assert (team_data.my_team() == 'FallsIA')
