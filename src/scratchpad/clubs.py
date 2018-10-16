import yaml

with open("src/scratchpad/clubs.yml", 'r') as teamfile:
    try:
        teamdata = yaml.load(teamfile)
        print(teamdata)
        print()
        print(teamdata["teams"])
        print()
        print(teamdata["me"])
        print()
        print(teamdata["start_time"])
        allteams = teamdata["teams"]
        for teamid in allteams:
            print("*")
            print(teamid)
            team_data = allteams[teamid]
#            print(team_data)
#            print(f"{teamid['name']}/{teamid['location']}")
            printing = (f"{team_data['name']}/{team_data['location']}")
            if "start_time" in team_data:
                printing = (f"{printing}/{team_data['start_time']}")
            print(printing)
    except yaml.YAMLError as exc:
        print(exc)
