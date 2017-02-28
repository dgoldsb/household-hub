'''
Sends around reminders
'''
from __future__ import print_function
import sqlite3
import os
import csv
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

def send_mail(send_from, recipients, subject, text, filename, pwd):
    '''
    Sends email, recipients is a list
    '''
    recipients = recipients
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['Reply-to'] = send_from
    msg.preamble = 'Multipart message...\n'
    part = MIMEText(text)
    msg.attach(part)
    if filename is not None:
        part = MIMEText("\nPlease find the attached file")
        msg.attach(part)
        part = MIMEApplication(open(filename, "rb").read())
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login(send_from, pwd)
    server.sendmail(msg['From'], emaillist, msg.as_string())

def sendalert(parent, address, recipient):
    '''
    Sends alerts to someone with a chore coming up the next day
    '''
    body = "Yo "+recipient+", vergeet niet dat je dit moet gaan doen (zie titel)!"

    sender_address = None
    pwd = None
    with open(os.path.join(ROOT, 'scripts/email.csv'), 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            sender_address = row[0]
            pwd = row[1]
    print(sender_address, [address], parent, body, None, pwd)
    send_mail(sender_address, [address], parent, body, None, pwd)
    return 0


def findalerts():
    '''
    Send all alerts
    '''
    conn = sqlite3.connect(os.path.join(ROOT, 'database/hub.db'))
    conn.text_factory = str
    curs = conn.cursor()

    # Send reminders for chores that are today
    job = "SELECT c.name, b.first_name, b.email FROM (SELECT * FROM chorelog "\
          "WHERE date_todo == DATE('now') AND finished = 0) as a "\
          "LEFT JOIN (SELECT * FROM housemates) as b ON a.UID = b.UID "\
          "LEFT JOIN (SELECT * FROM chores) as c ON a.CID = c.CID"
    curs.execute(job)
    reminders = curs.fetchall()
    for reminder in reminders:
        print('Sending reminder to %s (%s) about %s...' % reminder)
        sendalert(reminder[0], reminder[2], reminder[1])

    # Send reminders for chores that are almost overdue
    job = "SELECT c.name, b.first_name, b.email FROM (SELECT * FROM chorelog "\
          "WHERE date_todo == DATE('now', '-1 day') AND finished = 0) as a "\
          "LEFT JOIN (SELECT * FROM housemates) as b ON a.UID = b.UID "\
          "LEFT JOIN (SELECT * FROM chores) as c ON a.CID = c.CID"

    curs.execute(job)
    reminders = curs.fetchall()
    for reminder in reminders:
        if reminder[2] is not None:
            sendalert(reminder[0], reminder[2], reminder[1])

    # TODO: Send reminders for reminders

    return 0

def main():
    '''
    Main function
    '''
    findalerts()


if __name__ == "__main__":
    main()
