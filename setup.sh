a="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p database

# Build and fill the database if it does not exist
if [ ! -f $a/database/hub.db ]; then
    sqlite3 $a/database/hub.db < $a/scripts/setupDB.sql
    sqlite3 $a/database/hub.db < $a/scripts/initializeDB.sql
    python $a/scripts/updatedb.py
fi

# If cronjob does not exist for update (weekly), create
grep $USER+' python '+$a+'/scripts/updateDB.py' /etc/crontab || echo '0  12  *  *  1 '+$USER+' python '+$a+'/scripts/updateDB.py' >> /etc/crontab

# If cronjob does not exist for reminders (daily), create
grep $USER+' python '+$a+'/scripts/sendreminders.py' /etc/crontab || echo '0  12  *  *  * '+$USER+' python '+$a+'/scripts/sendreminders.py' >> /etc/crontab

# If cronjob does not exist for launching the flask page (startup), create
grep $USER+' python '+$a+'/app/hub/hub.py &' /etc/crontab || echo '@REBOOT '+$USER+' python '+$a+'/app/hub/hub.py &' >> /etc/crontab

# Reboot the machine for crontab to take effect
echo "Reboot the machine for everything to take effect."
read -p  "Do you want to reboot (y/n)? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo reboot
fi
