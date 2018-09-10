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
import smtplib
import logging
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..')
logging.basicConfig(filename=os.path.join(ROOT, 'hub.log'),
                    level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

def send_mail(send_from, recipients, subject, text, filename, pwd):
    '''
    Sends email, recipients is a list
    '''
    recipients = recipients
    logging.debug(recipients)
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

def sendalert(parent, address, recipient, admin):
    '''
    Sends alerts to someone with a chore coming up the next day
    '''
    body = "Yo "+recipient+", vergeet niet dat je moet schoonmaken (zie titel)!"

    sender_address = None
    pwd = None
    with open(os.path.join(ROOT, 'scripts/config.csv'), 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            sender_address = row[0]
            pwd = row[1]
    send_mail(sender_address, [address, admin], parent, body, None, pwd)
    return 0


def findalerts():
    '''
    Send all alerts
    '''
    conn = sqlite3.connect(os.path.join(ROOT, 'database/hub.db'))
    conn.text_factory = str
    curs = conn.cursor()

    # Find the admin
    job = "SELECT email FROM persons WHERE UID = 1"
    curs.execute(job)
    admin = curs.fetchall()[0][0]

    # Send reminders for chores that are today
    job = "SELECT c.name, b.first_name, b.email FROM (SELECT * FROM chorelog "\
          "WHERE date_todo == DATE('now') AND finished = 0) as a "\
          "LEFT JOIN (SELECT * FROM persons) as b ON a.UID = b.UID "\
          "LEFT JOIN (SELECT * FROM chores) as c ON a.CID = c.CID"
    curs.execute(job)
    reminders = curs.fetchall()
    for reminder in reminders:
        logging.info('Attempting to send early reminder')
        if reminder[2] is not None:
            logging.info('Sent reminder to '+str(reminder[1])+' ('\
                        +str(reminder[2])+') about '+str(reminder[0]))
            sendalert(reminder[0], reminder[2], reminder[1], admin)
        else:
            logging.info('No email address given')

    # Send reminders for chores that are almost overdue
    job = "SELECT c.name, b.first_name, b.email FROM (SELECT * FROM chorelog "\
          "WHERE date_todo == DATE('now', '-4 day') AND finished = 0) as a "\
          "LEFT JOIN (SELECT * FROM persons) as b ON a.UID = b.UID "\
          "LEFT JOIN (SELECT * FROM chores) as c ON a.CID = c.CID"

    curs.execute(job)
    reminders = curs.fetchall()
    for reminder in reminders:
        logging.info('Attempting to send late reminder')
        if reminder[2] is not None:
            logging.info('Sent reminder to '+str(reminder[1])+' ('\
                        +str(reminder[2])+') about '+str(reminder[0]))
            sendalert(reminder[0], reminder[2], reminder[1], admin)
        else:
            logging.info('No email address given')

    return 0

def main():
    '''
    Main function
    '''
    # Start logging
    logging.info('Attempting to send alerts')
    findalerts()


if __name__ == "__main__":
    main()
