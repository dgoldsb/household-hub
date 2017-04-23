'''
Update the database, weekly or daily cronjob
Done in Python because SQL server has stuff that I wanted to use, and SQLite does not have it
'''
from __future__ import print_function
import subprocess
import sqlite3
import time
import os
import csv
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import logging
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

def updatedb():
    '''
    Add chores for the upcoming 10 weeks that have not been planned yet
    '''
    conn = sqlite3.connect(os.path.join(ROOT, 'database/hub.db'))
    conn.text_factory = str
    curs = conn.cursor()

    # Get the first weekday date last week
    curs.execute("SELECT DATE('now','weekday 0','-6 day')")
    last_week = curs.fetchone()[0]

    dates = []
    for i in range(0, 10):
        shift = i*7-6
        if shift > 0:
            job = "SELECT DATE('now','weekday 0','+%d day')"
            curs.execute(job % shift)
        else:
            job = "SELECT DATE('now','weekday 0','-%d day')"
            curs.execute(job % abs(shift))
        dates.append(curs.fetchone()[0])

    curs.execute("SELECT date_todo, CID FROM chorelog WHERE date_todo"\
                 " > DATE('now','weekday 0','-8 day')")
    pairs_done = curs.fetchall()

    curs.execute('SELECT DISTINCT CID FROM chores')
    jobs = curs.fetchall()

    # Create counting table
    job = "INSERT INTO chores_unplanned SELECT UID, TID, CID,"\
          " date_todo FROM chorelog WHERE date_todo > '%s'"
    curs.execute(job % last_week)

    for date in dates:
        for chore in jobs:
            if (date, chore[0]) not in pairs_done:
                # Determine the correct teamID
                # Note that we order by no_jobs DESC, so if one team gets one they
                # get all they can do
                job = """SELECT     a.TID
                                   ,IFNULL(b.no_jobs,0) AS no_jobs
                                   ,IFNULL(d.last_job,'2000-12-12') AS last_job
                                   ,IFNULL(c.last_done,'2000-12-12') AS last_done
                         FROM      (SELECT DISTINCT TID 
                                    FROM team_chore
                                    WHERE CID = %d) AS a 
                         LEFT JOIN (SELECT TID, count(TID) no_jobs 
                                    FROM chores_unplanned 
                                    WHERE date_todo = '%s' AND TID IS NOT NULL 
                                    GROUP BY TID) AS b 
                         ON         a.TID = b.TID 
                         LEFT JOIN (SELECT TID, max(date_todo) AS last_done 
                                    FROM chorelog 
                                    WHERE CID = %d 
                                    GROUP BY TID) AS c 
                         ON         a.TID = c.TID 
                         LEFT JOIN (SELECT TID, max(date_todo) AS last_job 
                                    FROM chorelog GROUP BY TID) AS d 
                         ON         a.TID = d.TID 
                         ORDER BY   no_jobs DESC
                                   ,last_done ASC
                                   ,last_job ASC"""
                curs.execute(job % (chore[0], date, chore[0]))
                team = curs.fetchone()[0]

                # Add teamID to the where statement
                job = """SELECT     a.UID
                                   ,IFNULL(b.no_jobs,0) AS no_jobs
                                   ,IFNULL(d.last_job,'2000-12-12') AS last_job
                                   ,IFNULL(c.last_done,'2000-12-12') AS last_done
                         FROM      (SELECT UID FROM teams WHERE TID = %d) AS z
                         LEFT JOIN (SELECT DISTINCT UID 
                                    FROM housemates WHERE active = 1) AS a
                         ON         z.UID = a.UID
                         LEFT JOIN (SELECT UID, count(UID) no_jobs 
                                    FROM chores_unplanned 
                                    WHERE date_todo = '%s' AND UID IS NOT NULL 
                                    GROUP BY UID) AS b 
                         ON         a.UID = b.UID 
                         LEFT JOIN (SELECT UID, max(date_todo) AS last_done 
                                    FROM chorelog 
                                    WHERE CID = %d 
                                    GROUP BY UID) AS c 
                         ON         a.UID = c.UID 
                         LEFT JOIN (SELECT UID, max(date_todo) AS last_job 
                                    FROM chorelog GROUP BY UID) AS d 
                         ON         a.UID = d.UID 
                         ORDER BY   no_jobs ASC
                                   ,last_done ASC
                                   ,last_job ASC"""
                curs.execute(job % (team, date, chore[0]))
                assignee = curs.fetchone()[0]

                # Update in the table that we use to count the number of jobs this week
                job = "INSERT INTO chores_unplanned (UID, TID, CID, date_todo) VALUES ("\
                      +str(assignee)+","+str(team)+","+str(chore[0])+",'"+str(date)+"')"
                curs.execute(job)

                # Insert into chorelog
                job = "INSERT INTO chorelog (date_todo, CID, finished, UID, TID) "\
                      "VALUES ('"+str(date)+"', "+str(chore[0])+", 0, "+str(assignee)\
                      +", "+str(team)+")"
                curs.execute(job)
                logging.info('Executing: '+str(job))

    # Drop the counting table and commit database changes
    curs.execute('DELETE FROM chores_unplanned')
    conn.commit()
    return 0

def truncatedb():
    """
    Truncates the database, and rebuilds
    """
    conn = sqlite3.connect(os.path.join(ROOT, 'database/hub.db'))
    conn.text_factory = str
    curs = conn.cursor()

    # Get the first weekday date last week
    curs.execute("DELETE FROM chorelog WHERE date_todo > DATE('now','weekday 0','+7 day')")

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
    msg.preamble = text
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

def main():
    '''
    Calls all parts of the update
    '''
    # Start logging
    logging.basicConfig(filename=os.path.join(ROOT, 'hub.log'),
                        level=logging.INFO, format='%(asctime)s %(message)s')

    # Backup
    if os.path.isfile(os.path.join(ROOT, 'database/hub.db')):
        bufile = os.path.join(ROOT, 'database/hub_'+str(time.strftime("%c"))+'.db')
        logging.info('Backing database up to '+str(bufile))
        debug = subprocess.check_output(['cp', '-f', os.path.join(ROOT, 'database/hub.db')
                                         , bufile])

        address = None
        pwd = None
        admin = None
        with open(os.path.join(ROOT, 'scripts/email.csv'), 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                address = row[0]
                pwd = row[1]
                admin = row[2]
                break
        send_mail(address, [admin], 'Backup '+bufile, 'See attachment.', bufile, pwd)
        logging.debug(debug)

    # Truncate (in case housemates leave, make sure all weeks are recomputed)
    truncatedb()
    logging.info('Truncated database')
    # Do the update
    updatedb()
    logging.info('Updated database')

if __name__ == "__main__":
    main()
