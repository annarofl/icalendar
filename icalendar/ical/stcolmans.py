from icalendar import Calendar
from ical import bowls_funcs


year = '2017-18'
me = 'stcolmans'
bowls_funcs.init(me, year)

json_teamdata = bowls_funcs.load_json('%s_teams.json' % me)
json_matchdata = bowls_funcs.load_json('%s_matches_%s.json' % (me,year))

cal = Calendar()
# pre-reqs
cal.add('prodid', '-//Bowling Calendar//mc-williams.co.uk//')
cal.add('version', '2.0')
cal.add('calscale', 'GREGORIAN')
cal.add('X-WR-TIMEZONE', 'Europe/London')

team_data = json_teamdata['teams']
for match in json_matchdata['matches']:
    cal.add_component(bowls_funcs.create_event(match, team_data))

bowls_funcs.print_cal( cal )
bowls_funcs.write_file( '%s_%s' % (me,year), cal )
