from .context import TeamData

# from ical.match import Match
import collections
from collections import OrderedDict


def _generate_team(location: str, name: str, start_time: str = None) -> OrderedDict:
    team_data = collections.OrderedDict()
    team_data['location'] = location
    team_data['name'] = name
    if start_time is not None:
        team_data['start_time'] = start_time
    return team_data


def test_team_data() -> OrderedDict:
    data = collections.OrderedDict()
    data['me'] = 'TEAMME'
    data['start_time'] = '19:30'
    team = collections.OrderedDict()
    team['TEAM1'] = _generate_team('location 1', 'team 1')
    team['TEAM2'] = _generate_team('location 2', 'team 2', '20:00')
    team['TEAMME'] = _generate_team('TeamMe Location', 'TeamMe')
    team['FALLSA'] = _generate_team('FallsA location', 'Falls A')
    data['teams'] = team

    return data


def fallsa_test_data() -> OrderedDict:
    data = collections.OrderedDict()
    data['me'] = 'FALLSA'
    data['start_time'] = '19:30'
    team = collections.OrderedDict()
    team['TEAM1'] = _generate_team('location 1', 'team 1')
    team['TEAM2'] = _generate_team('location 2', 'team 2', '20:00')
    team['TEAMME'] = _generate_team('TeamMe Location', 'TeamMe')
    team['FALLSA'] = _generate_team('FallsA location', 'Falls A')
    team['DUNBA'] = _generate_team('DUNBA location', 'Dunbarton')
    team['OLDLA'] = _generate_team('OLDLA location', 'Old Bleach A')
    data['teams'] = team

    return data
