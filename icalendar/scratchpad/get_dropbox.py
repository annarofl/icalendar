"""
%APPDATA%\Dropbox\info.json
%LOCALAPPDATA%\Dropbox\info.json

{
    {"personal":
            {"path": "/Users/<username>/Dropbox (Personal)",
            "host": 3721379913, 
            "is_team": false, 
            "subscription_type": "Basic"},
     {"business": 
            {"path": "/Users/<username>/Dropbox (<business name>)", 
            "host": 3286328207, 
            "is_team": true, 
            "subscription_type": "Business"}
}

{"personal": {"path": "E:\\Users\\gmcwilliams\\Dropbox", "host": 3464053134, "is_team": false, "subscription_type": "Basic"}}

"""

import os
from pathlib import Path
import json

try:
    json_path = (Path(os.getenv('LOCALAPPDATA'))/'Dropbox'/'info.json').resolve()
except FileNotFoundError:
    json_path = (Path(os.getenv('APPDATA'))/'Dropbox'/'info.json').resolve()

with open(str(json_path)) as f:
    j = json.load(f)

personal_dbox_path = Path(j['personal']['path'])

print(personal_dbox_path)
