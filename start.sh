#!/bin/bash

export MAX_SIZE=10M

# change into the script dir
cd $(dirname $0)

# check if log file is greater then MAX_SIZE, if yes delete it
find ./inwx-update.log -size +$MAX_SIZE -exec rm -f {} \;

# run the update script and pipe its output to the log file
python inwx-update.py | tee -a inwx-update.log

unset MAX_SIZE
