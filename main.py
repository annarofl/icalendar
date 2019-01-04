from ical.events import Events

import argparse
import os

parser = argparse.ArgumentParser(description="Process Bowls matches.")
parser.add_argument("-t", "--team")
parser.add_argument("-y", "--year")

args = parser.parse_args()

team = args.team if args.team is not None else os.environ['ICAL_TEAM']
year = args.year if args.year is not None else os.environ['ICAL_YEAR']

events = Events(team, year)

events.add_events()
