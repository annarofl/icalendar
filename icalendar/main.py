from ical.events import Events

import argparse
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description='Process Bowls matches.')
parser.add_argument('-t', '--team')
parser.add_argument('-y', '--year')

args = parser.parse_args()

checkFile = Path('data', args.team, ('%s_matches_%s.json' % (args.team, args.year)))
if (not checkFile.exists()):
    print("Cannot find data for %s/%s" % (args.team, args.year))
    sys.exit(1)

events = Events(args.team, args.year)

events.add_events()
