a="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p database

# Build and fill the database if it does not exist
if [ ! -f $a/database/hub.db ]; then
    sqlite3 $a/database/hub.db < $a/scripts/setupDB.sql
    sqlite3 $a/database/hub.db < $a/scripts/initializeDB.sql
    python $a/scripts/updatedb.py
fi

# Add cronjobs
(crontab -l 2>/dev/null; echo "0  12  *  *  * /bin/bash "+$a+"/scripts/remind.sh") | crontab -
(crontab -l 2>/dev/null; echo "0  12  *  *  1 /bin/bash "+$a+"/scripts/update.sh") | crontab -
echo "Check for duplicate cronjob manually so far"

# Set up supervisorcls
echo "Set up supervisor manually to run launcher.sh"

# Reboot the machine for crontab to take effect
echo "Reboot the machine for everything to take effect."
read -p  "Do you want to reboot (y/n)? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo reboot
fi
