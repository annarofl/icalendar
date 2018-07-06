from ical.events import Events

import argparse

from envparse import Env
DATAPATH="gary"
env = Env(
    TEAM=str,
    YEAR=str,
    DATAPATH=str,
)
env.read_envfile()

print(f"DATAPATH={DATAPATH}")

parser = argparse.ArgumentParser(description="Process Bowls matches.")
parser.add_argument("-t", "--team")
parser.add_argument("-y", "--year")

args = parser.parse_args()

events = Events(args.team, args.year)

events.add_events()
