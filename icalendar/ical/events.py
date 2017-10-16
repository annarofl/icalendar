'''
Created on 11 Oct 2017

@author: gmcwilliams
'''
from icalendar import Calendar
import json
from datetime import timedelta, datetime
from icalendar.cal import Event
from tempfile import gettempdir
import os

class Events:
    '''
    Manage calendar events
    '''


    def __init__(self, club, year):
        '''
        Constructor
        '''

        self.club = club
        self.year = year
                
        self.cal = Calendar()
        self.cal.add('prodid', '-//Bowling Calendar//mc-williams.co.uk//')
        self.cal.add('version', '2.0')
        self.cal.add('calscale', 'GREGORIAN')
        self.cal.add('X-WR-TIMEZONE', 'Europe/London')

        self.json_matchdata = self._load_json('%s_matches_%s.json' % (club, year))
        
        json_teamdata = self._load_json('%s_teams.json' % club)
        self.team_data = json_teamdata['teams']
        self.myclub = json_teamdata['me'] 
    
    def add_events(self):
        for match in self.json_matchdata['matches']:
            self.cal.add_component(self._create_event(match))

        self._print_cal()
        self._write_file()

    def _load_json(self, json_filename):
        "loads the JSON file"
        with open(json_filename) as data_file:    
            json_data = json.load(data_file)
        # print(json.dumps(json_data, indent=2))
        # print(json_data['matches'])
        return json_data;
    
    def _create_event(self, match_data):
    #    print(match_data)
    #    print(team_data)
        match = Match(match_data, self.team_data, self.myclub)

        event = Event()
        event['uid'] = match.id(self.year)
        event['location'] = match.location
        event.add('priority', 5)
    
        event.add('summary', match.summary())
        event.add('description', match.description())
        event.add('dtstart', match.match_start)
        event.add('dtend', match.match_end)
        event.add('dtstamp', datetime.utcnow())
        
        return event

    def _mk_save_dir(self):    
        newdir = os.path.join(gettempdir(), 'icalendar') 
        if not os.path.exists(newdir):
            os.makedirs(newdir)
        return newdir
    
    def _write_file(self):
        filename = '%s_%s' % (self.club, self.year)
        newfile = os.path.join(self._mk_save_dir(), '%s.ics' % filename)
        f = open(newfile, 'wb')
        f.write(self.cal.to_ical())
        f.close()
        print('saved:' + newfile)
    
    def _print_cal(self):
        print(self.cal.to_ical())


class Match:
    '''
    Manage one match
    '''

    def __init__(self, match_data, team_data, myclub):
        '''
        Constructor
        '''

        self.match_data = match_data
        self.team_data = team_data
        self.myclub = myclub
        home = self.team_data[match_data['home']]
        away = self.team_data[match_data['away']]
        self.home_team = home['name']
        self.home_score = match_data['home_score']
        self.away_team = away['name']
        self.away_score = match_data['away_score']
        self.location = home['location']
        self.date_fmt_in = '%Y-%m-%d_%H:%M'
        self.match_start = datetime.strptime(match_data['date'], self.date_fmt_in)
        self.match_end = self.match_start + timedelta(hours=+3)
        self.label = ''
        if ('label' in match_data):
            self.label = ' (%s)' % (match_data['label'])
    
    def summary(self):
        summary = '%s (%s) v (%s) %s%s' % (self.home_team, self.home_score,
                                         self.away_score, self.away_team, self.label)
        return summary

    def description(self):    
        display_date = self.match_start.strftime(self.date_fmt_in)
        description = '%-12s (%2s) v (%2s) %-12s on %s%s' % (self.home_team, self.home_score,
                                                           self.away_score, self.away_team,
                                                           display_date, self.label)
        print(description)
        return description

    def id(self, year):
        id_club = '%s-%s' % (self.match_data['home'],'AWAY')
        if (self.match_data['home'] == self.myclub):
            id_club = '%s-%s' % (self.match_data['away'],'HOME')

        return '%s-%s-%s%s@mc-williams.co.uk' % (self.myclub, year, id_club, self.label)
