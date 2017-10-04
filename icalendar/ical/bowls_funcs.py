import json
from datetime import datetime, timedelta

from icalendar import Event
import pytz, os
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
#    print(match_data['home'])
#    print(team_data)
    """Create an event for the given match_data"""
    home = match_data['home']
    away = match_data['away']
    for team in team_data:
        if team['id'] == match_data['home']:
            home = team['name']
            location = team['location']
        if team['id'] == match_data['away']:
            away = team['name']

    fmt_in = '%Y-%m-%d_%H:%M'
    fmtical = '%Y%m%dT%H%M00Z'
    match_date = datetime.strptime(match_data['date'], fmt_in)
    end_date = match_date + timedelta(hours=+3)
    display_date = match_date.strftime(fmt_in)
    idate = match_date.strftime(fmtical)
    print('%-10s v %-10s on %s' % (home,away, display_date))
    event = Event()
    event['uid'] = '%s%s@mc-williams.co.uk' % (idate, home)
    event['location'] = location
    event.add('priority', 5)

    event.add('summary', '%s v %s' % (home,away))
    event.add('dtstart', match_date)
    event.add('dtend', end_date)
    event.add('dtstamp', datetime(2005, 4, 4, 0, 10, 0, tzinfo=pytz.utc))
    
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
