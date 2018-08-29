#!/bin/bash
#
# Crontab entry
# */2 * * * * /root/block_bad_auth_cron.sh > /var/log/block_bad_auth_cron.log
date "+timestamp: %Y-%m-%d %H:%M:%S"
(

    echo "Checking for lock. If lock, will wait 10s"
    # Wait for lock on /var/lock/.block_bad_auth_cron_lock
    flock -x -w 10 200 || exit 1
    . /root/.cronenv

    /root/block_bad_auth.py
    echo "Done inside"

    /bin/sleep 10
    /root/block_bad_auth.py
    echo "Done inside 2 (after 10 seconds)"

    /bin/sleep 10
    /root/block_bad_auth.py
    echo "Done inside 3 (after 20 seconds)"

    /bin/sleep 10
    /root/block_bad_auth.py
    echo "Done inside 4 (after 30 seconds)"            

) 200>/var/lock/.block_bad_auth_cron_lock

echo "Done outside"
