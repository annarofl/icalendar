import json
from datetime import datetime, timedelta

from icalendar import vCalAddress, vText
from icalendar import vDatetime, Calendar, Event
import pytz, os
from tempfile import gettempdir
from re import match

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

def write_file( cal ):
    newfile = os.path.join(mk_save_dir(), '%s_%s.ics' % (me,year))
    f = open(newfile, 'wb')
    f.write(cal.to_ical())
    f.close()
    print('saved:' + newfile)

def print_cal( cal ):
    print(cal.to_ical())

year = '2017-18'
me = 'fallsindoor'
json_teamdata = load_json('%s_teams.json' % me)
json_matchdata = load_json('%s_matches_%s.json' % (me,year))

cal = Calendar()
# pre-reqs
cal.add('prodid', '-//Bowling Calendar//mc-williams.co.uk//')
cal.add('version', '2.0')
cal.add('calscale', 'GREGORIAN')
cal.add('X-WR-TIMEZONE', 'Europe/London')

team_data = json_teamdata['teams']
for match in json_matchdata['matches']:
    cal.add_component(create_event(match, team_data))

print_cal( cal )
write_file( cal )
