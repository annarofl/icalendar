import json
from datetime import datetime

from icalendar import vCalAddress, vText
from icalendar import vDatetime, Calendar, Event
import pytz, os
from tempfile import gettempdir

with open('teams.json') as data_file:    
    json_data = json.load(data_file)
print(json.dumps(json_data, indent=2))

#print json_data['data']
print(json_data['teams'])
# {'251228454889939/insights/page_fan_adds_unique/day': ...

cal = Calendar()
# pre-reqs
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

for team in json_data['teams']:
    print(team['name'])
    event = Event()
    event['uid'] = '20050115T101010/27346262376@mxm.dk'
    event['location'] = team['location']
    event.add('priority', 5)

    event.add('summary', 'Match against %s' % team['name'])
    event.add('dtstart', datetime(2005, 4, 4, 8, 0, 0, tzinfo=pytz.utc))
    event.add('dtend', datetime(2005, 4, 4, 10, 0, 0, tzinfo=pytz.utc))
    event.add('dtstamp', datetime(2005, 4, 4, 0, 10, 0, tzinfo=pytz.utc))

    cal.add_component(event)

newdir = os.path.join(gettempdir(), 'icalendar') 
newfile = os.path.join(newdir, 'falls.ics')
if not os.path.exists(newdir):
    os.makedirs(newdir)
f = open(newfile, 'wb')
f.write(cal.to_ical())
f.close()
print('saved:' + newfile)
