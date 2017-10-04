import json
from datetime import datetime

from icalendar import vCalAddress, vText
from icalendar import vDatetime, Calendar, Event
import pytz, os
from tempfile import gettempdir

def load_json( json_filename ):
    "loads the JSON file"
    with open(json_filename) as data_file:    
        json_data = json.load(data_file)
    #print(json.dumps(json_teamdata, indent=2))
    return json_data;

def create_event( event_data ):
    """Create an event for the given event_data"""
    print(team['name'])
    event = Event()
    event['uid'] = '20050115T101010/27346262376@mxm.dk'
    event['location'] = event_data['location']
    event.add('priority', 5)

    event.add('summary', 'Match against %s' % event_data['name'])
    event.add('dtstart', datetime(2005, 4, 4, 8, 0, 0, tzinfo=pytz.utc))
    event.add('dtend', datetime(2005, 4, 4, 10, 0, 0, tzinfo=pytz.utc))
    event.add('dtstamp', datetime(2005, 4, 4, 0, 10, 0, tzinfo=pytz.utc))
    
    return event

def mk_save_dir():    
    newdir = os.path.join(gettempdir(), 'icalendar') 
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    return newdir


json_teamdata = load_json('teams.json')

cal = Calendar()
# pre-reqs
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

for team in json_teamdata['teams']:
    cal.add_component(create_event(team))

newfile = os.path.join(mk_save_dir(), 'falls.ics')
f = open(newfile, 'wb')
f.write(cal.to_ical())
f.close()
print('saved:' + newfile)
