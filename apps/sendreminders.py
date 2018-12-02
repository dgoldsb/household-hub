"""
Sends around reminders.
"""

from __future__ import print_function
import sqlite3
import os
import csv
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import logging

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
logging.basicConfig(filename=os.path.join(ROOT, 'hub.log'),
                    level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def find_alerts():
    """
    Find and return the list of alerts that should be send out. The returned values is a list of lists, where each
    inner lists contains three items:

    - the name of the chore
    - the name of person who should do the chore
    - the email address of the person who should do the chore

    :returns: a list of alerts to send (type=list(list)))
    """
    conn = sqlite3.connect(os.path.join(ROOT, 'database/hub.db'))
    conn.text_factory = str
    curs = conn.cursor()

    # Query for chores that are starting their 'to do'-window or that are almost overdue.
    job = """
        SELECT
            c.name,
            b.first_name,
            b.email
        FROM (
            SELECT *
            FROM chorelog
            WHERE date_todo == DATE('now') OR date_todo == DATE('now', '+1 day')
            ) AS a
            LEFT JOIN (
                SELECT * 
                FROM housemates
                ) AS b 
            ON a.UID = b.UID
            LEFT JOIN (
                SELECT *
                FROM chores
                ) AS c
            ON a.CID = c.CID"""

    # Find and return the resulting jobs.
    curs.execute(job)
    return curs.fetchall()


def send_alert(chore, recipient_address, recipient_name, template='reminder_template_NL.txt'):
    """
    Sends alerts to someone regarding a chore. We are smart and do not store credentials in GitHub, so make sure you
    create the file ROOT/config.csv locally with the following contents:

    {EMAIL},{PASSWORD}

    :param chore: the name of the chore (type=str)
    :param recipient_address: the email address of the person who should be reminded (type=str)
    :param recipient_name: the name of the person who should be reminded (type=str)
    :param template: the name of the template of the email body, default is Dutch (type=str)
    """
    # Open and fill in the template.
    with open(os.path.join(ROOT, 'apps', 'templates', template)) as file:
        body = file.read().format(chore=chore.lower(), recipient=recipient_name)

    # Load our sender config.
    sender_address = None
    pwd = None
    with open(os.path.join(ROOT, 'config.csv'), 'rb') as config:
        reader = csv.reader(config, delimiter=',')
        for row in reader:
            sender_address = row[0]
            pwd = row[1]
            
    # Send the email.
    send_mail(sender_address, [recipient_address], chore, body, pwd)


def send_mail(send_from, recipients, subject, text, pwd, filename=None):
    """
    Send an email.
    
    :param send_from: the senders email address (type=str)
    :param recipients: the recipients email addresses (type=list(str))
    :param subject: the subject of the email (type=str)
    :param text: the body of the email (type=str)
    :param pwd: the password to the send_from email (type=str)
    :param filename: the path to a file to include in the email, optional (type=str)
    """
    recipients = recipients
    logging.debug(recipients)
    email_list = [elem.strip().split(',') for elem in recipients]

    # Set up the message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['Reply-to'] = send_from
    msg.preamble = 'Multipart message...\n'
    part = MIMEText(text)
    msg.attach(part)

    # Attach a file.
    if filename is not None:
        part = MIMEText("\nPlease find the attached file")
        msg.attach(part)
        part = MIMEApplication(open(filename, "rb").read())
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)

    # Send the email.
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login(send_from, pwd)
    server.sendmail(msg['From'], email_list, msg.as_string())


if __name__ == "__main__":
    # Fetch all the reminders that should be sent out.
    reminders = find_alerts()

    # Send each reminder.
    for reminder in reminders:
        logging.info('Attempting to send late reminder.')
        if reminder[2] is not None:
            logging.info('Sent reminder to {} about {}'.format(reminder[1], reminder[0]))
            send_alert(reminder[0], reminder[2], reminder[1])
        else:
            logging.info('No email address given.')
