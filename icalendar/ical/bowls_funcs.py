import json
from datetime import datetime, timedelta

from icalendar import Event
import os
from tempfile import gettempdir

_club = ""
_year = ""


def init(club, year):
    _club = club
    _year = year
    
def load_json( json_filename ):
    "loads the JSON file"
    with open(json_filename) as data_file:    
        json_data = json.load(data_file)
    #print(json.dumps(json_data, indent=2))
    #print(json_data['matches'])
    return json_data;

def create_event( match_data, team_data ):
#    print(match_data)
#    print(team_data)
    """Create an event for the given match_data"""
    home = team_data[match_data['home']]
    away = team_data[match_data['away']]
    home_team = home['name']
    home_score = match_data['home_score']
    away_team = away['name']
    away_score = match_data['away_score']
    location = home['location']
    
    date_fmt_in = '%Y-%m-%d_%H:%M'
    match_start = datetime.strptime(match_data['date'], date_fmt_in)
    match_end = match_start + timedelta(hours=+3)

    date_fmt_ical = '%Y%m%dT%H%M00Z'
    display_date = match_start.strftime(date_fmt_in)
    idate = match_start.strftime(date_fmt_ical)
    description = '%-12s (%2s) v (%2s) %-12s on %s' % (home_team,home_score,away_score,away_team, display_date)
    print(description)
    event = Event()
    event['uid'] = '%s%s@mc-williams.co.uk' % (idate, match_data['home'])
    event['location'] = location
    event.add('priority', 5)

    event.add('summary', '%s v %s' % (home_team,away_team))
    event.add('description', description)
    event.add('dtstart', match_start)
    event.add('dtend', match_end)
    event.add('dtstamp', datetime.utcnow())
    
    return event

def mk_save_dir():    
    newdir = os.path.join(gettempdir(), 'icalendar') 
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    return newdir

def write_file( filename, cal ):
    newfile = os.path.join(mk_save_dir(), '%s.ics' % filename)
    f = open(newfile, 'wb')
    f.write(cal.to_ical())
    f.close()
    print('saved:' + newfile)

def print_cal( cal ):
    print(cal.to_ical())
