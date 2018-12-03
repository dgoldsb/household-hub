# Super Simple Scheduler

**Disclaimer**: I wrote this as a joke project waaaaay back when I was first trying out `Flask`/`SQLite`.
I cleaned it up a bit later because this project did find use, but it is a bit of a mess as a result, and is not intended to be a stellar project.

## Introduction

I would have called it S3, damn Amazon.

This is a Python Flask page to run on a local network on a Raspberry Pi, made for me and my housemates to keep track of who does what chores and all.
I use a SQLite for storage.
It is a bit shoddy programming, I wrote this once to get acquinted with Flask and kept using it because it was the only way to make my housemates do their stuff.

## Setup

Do some DBAing and enter the chores and people in the respective tables.

Run the setup.sh procedure in the root directory to setup the database, add the cronjobs, and reboot the system.
After reboot, the Flask server launches on startup.
Add the email address, password, and admin email address (backups will be sent to this email) to the file `./scripts/config.csv`.
Make sure that you added the IP of your Pi in the `app.py` script.
