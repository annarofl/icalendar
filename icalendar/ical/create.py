#!/usr/bin/env python
# encoding: utf-8
'''
ical.create -- create a calendar file

@author:     Gary McWilliams

@copyright:  2015 Gary McWilliams. All rights reserved.

@license:    apache 2.0

@deffield    updated: Updated
'''

from datetime import datetime

from icalendar import vCalAddress, vText
from icalendar import vDatetime, Calendar, Event
import pytz

__all__ = []
__version__ = 0.1
__date__ = '2017-09-30'
__updated__ = '2017-09-30'

DEBUG = 1
TESTRUN = 0
PROFILE = 0


cal = Calendar()
# pre-reqs
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

event = Event()
event['location'] = vText('Odense, Denmark')
event['uid'] = '20050115T101010/27346262376@mxm.dk'
event.add('priority', 5)

event.add('summary', 'Python meeting about calendaring')
event.add('dtstart', datetime(2005, 4, 4, 8, 0, 0, tzinfo=pytz.utc))
event.add('dtend', datetime(2005, 4, 4, 10, 0, 0, tzinfo=pytz.utc))
event.add('dtstamp', datetime(2005, 4, 4, 0, 10, 0, tzinfo=pytz.utc))

organizer = vCalAddress('MAILTO:noone@example.com')
organizer.params['cn'] = vText('Max Rasmussen')
organizer.params['role'] = vText('CHAIR')
event['organizer'] = organizer

attendee = vCalAddress('MAILTO:maxm@example.com')
attendee.params['cn'] = vText('Max Rasmussen')
attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
event.add('attendee', attendee, encode=0)

attendee = vCalAddress('MAILTO:the-dude@example.com')
attendee.params['cn'] = vText('The Dude')
attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
event.add('attendee', attendee, encode=0)

cal.add_component(event)

f = open('example.ics', 'wb')
f.write(cal.to_ical())
f.close()
