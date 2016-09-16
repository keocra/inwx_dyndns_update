# Simple DynDNS update tool for self-owned INWX domains

Usage:
* Run get-dependencies.sh to clone the inwx python library (Commit #af81cb860b9226354efc8984de08ad101795227d)
* Run ```pip install commentjson```
* Edit the inwx-update.json file in the current directory
* Run ```python inwx-update.py```

Additional steps:
* You may want to add a crontab entry to automate the update at a regular basis (see example_crontab_entry.txt for help)
