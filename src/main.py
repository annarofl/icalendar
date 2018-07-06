from ical.events import Events

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Process Bowls matches.")
parser.add_argument("-t", "--team")
parser.add_argument("-y", "--year")

args = parser.parse_args()

events = Events(args.team, args.year)

events.add_events()
