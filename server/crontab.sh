#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "* * * * * /usr/bin/python3.5 $DIR/webscraper/webscraper.py >/dev/null 2>&1" > crontab.txt
crontab crontab.txt
