#!/usr/bin/env python
# encoding: utf-8
'''
ical.readcalendar -- Read a calendar file and print contents

@author:     Gary McWilliams

@copyright:  2015 Gary McWilliams. All rights reserved.

@license:    apache 2.0

@deffield    updated: Updated
'''

from icalendar import Calendar, Event


__all__ = []
__version__ = 0.1
__date__ = '2015-03-06'
__updated__ = '2015-03-06'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

# read the data from the file
data = open('FallsIndoor@group.calendar.google.com.ics').read()

g = open('Falls Indoor@group.calendar.google.com.ics', 'rb')
gcal = Calendar.from_ical(g.read())
for component in gcal.walk('vevent'):
    print('summary "{}"'.format(component.get('summary')))
    print('start "{}"'.format(component.get('dtstart')))
    print('end "{}"'.format(component.get('dtend')))
    print('stamp "{}"'.format(component.get('dtstamp')))
g.close()
