import json
from datetime import datetime

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
    home = away = "UNKNOWN"
    for team in team_data:
        if team['id'] == match_data['home']:
            home = team['name']
        if team['id'] == match_data['away']:
            away = team['name']
            
    print('Match %s v %s on %s' % (home,away, match_data['date']))
    event = Event()
    event['uid'] = '20050115T101010/27346262376@mxm.dk'
    #event['location'] = match_data['location']
    event.add('priority', 5)

    event.add('summary', 'Match %s v %s' % (home,away))
    event.add('dtstart', datetime(2005, 4, 4, 8, 0, 0, tzinfo=pytz.utc))
    event.add('dtend', datetime(2005, 4, 4, 10, 0, 0, tzinfo=pytz.utc))
    event.add('dtstamp', datetime(2005, 4, 4, 0, 10, 0, tzinfo=pytz.utc))
    
    return event

def mk_save_dir():    
    newdir = os.path.join(gettempdir(), 'icalendar') 
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    return newdir

def write_file( cal ):
    newfile = os.path.join(mk_save_dir(), 'falls.ics')
    f = open(newfile, 'wb')
    f.write(cal.to_ical())
    f.close()
    print('saved:' + newfile)

def print_cal( cal ):
    print(cal.to_ical())


json_data = load_json('falls.json')

cal = Calendar()
# pre-reqs
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

team_data = json_data['teams']
for match in json_data['matches']:
    cal.add_component(create_event(match, team_data))

print_cal( cal )
#write_file( cal )
