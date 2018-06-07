from ical.events import Events

import argparse
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description="Process Bowls matches.")
parser.add_argument("-t", "--team")
parser.add_argument("-y", "--year")

args = parser.parse_args()

filename = f"{args.team}_matches_{args.year}.json"
checkFile = Path("data", args.team, filename)
if not checkFile.exists():
    print(f"Cannot find data for {checkFile}")
    sys.exit(1)

events = Events(args.team, args.year)

events.add_events()
