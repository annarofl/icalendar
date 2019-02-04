from strictyaml import load, Map, Str, Int, Seq, YAMLError
from pathlib import Path

ymldata = open(Path("src/scratchpad/clubs.yml"), 'r').read()
print(ymldata)
print()
teamdata = load(ymldata)
# print(teamdata["teams"])
# print()
# print(teamdata["me"])
# print()
# print(teamdata["start_time"])
allteams = teamdata["teams"]
for teamid in allteams:
    print("*" * 8)
    print(teamid)
    team_data = allteams[teamid]
#            print(team_data)
#            print(f"{teamid['name']}/{teamid['location']}")
    printing = (f"{team_data['name']}/{team_data['location']}")
    if "start_time" in team_data:
        printing = (f"{printing}/{team_data['start_time']}")
    print(printing)
