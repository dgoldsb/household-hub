# household-hub

## Introduction

Python Flask page to run on a local network on a Raspberry Pi, made for me and my housemates to keep track of who does what chores and all.
Uses Flask for the webpage, and whatever database backend is easy to use in the back (mySQL is tempting).

## Setup

Run the setup.sh procedure in the root directory to setup the database, add the cronjobs, and reboot the system. After reboot, the Flask server launches on startup. Add the email address, password, and admin email address (backups will be sent to this email) to the file ./scripts/email.csv. Make sure that you added the IP of your Pi in the hub.py script. I will work later on building a proper config file, if anyone takes interest in this. Text is in Dutch so far, again something I should take out of the scripts/HTML templates as much as possible, and put in a config file.
