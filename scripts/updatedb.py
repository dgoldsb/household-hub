'''
Update the database, weekly or daily cronjob
Done in Python because SQL server has stuff that I wanted to use, and SQLite does not have it
'''

import csv
import sqlite3

def updatedb():
    '''
    Add chores for the upcoming 10 weeks that have not been planned yet
    '''
    conn = sqlite3.connect('hub.db')
    conn.text_factory = str
    curs = conn.cursor()

    # Get the first weekday date last week
    curs.execute("SELECT DATE('now','weekday 0','-8 day')")
    last_week = curs.fetchone()[0]

    dates = []
    for i in range(0, 10):
        shift = i*7-1
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

    curs.execute('SELECT DISTINCT UID FROM housemates')
    housemates = curs.fetchall()

    # Create counting table
    job = "INSERT INTO chores_unplanned SELECT UID, CID,"\
          " date_todo FROM chorelog WHERE date_todo > '%s'"
    curs.execute(job % last_week)

    for date in dates:
        for chore in jobs:
            if (date, chore[0]) not in pairs_done:
                job = "SELECT a.UID, IFNULL(b.no_jobs,0) AS no_jobs, "\
                      "IFNULL(d.last_job,'2000-12-12') AS last_job, "\
                      "IFNULL(c.last_done,'2000-12-12') AS last_done "\
                      "FROM (SELECT DISTINCT UID FROM housemates WHERE active = 1) AS a "\
                      "LEFT JOIN (SELECT UID, count(UID) no_jobs FROM chores_unplanned "\
                      "WHERE date_todo = '%s' AND UID IS NOT NULL "\
                      "GROUP BY UID) AS b ON a.UID = b.UID "\
                      "LEFT JOIN (SELECT UID, max(date_todo) AS last_done "\
                      "FROM chorelog WHERE CID = %d GROUP BY UID) AS c ON a.UID = c.UID "\
                      "LEFT JOIN (SELECT UID, max(date_todo) AS last_job "\
                      "FROM chorelog GROUP BY UID) AS d "\
                      "ON a.UID = d.UID ORDER BY no_jobs ASC, last_done ASC, last_job ASC"
                curs.execute(job % (date, chore[0]))
                assignee = curs.fetchone()[0]

                # Update in the table that we use to count the number of jobs this week
                job = "INSERT INTO chores_unplanned (UID, CID, date_todo) VALUES ("+str(assignee)+\
                      ","+str(chore[0])+",'"+str(date)+"')"
                curs.execute(job)

                # Insert into chorelog
                job = "INSERT INTO chorelog (date_todo, CID, finished, UID) "\
                      "VALUES ('"+str(date)+"', "+str(chore[0])+", 0, "+str(assignee)+")"
                curs.execute(job)
                print(job)

    # Drop the counting table and commit database changes
    curs.execute('DELETE FROM chores_unplanned')
    conn.commit()
    return 0

def sendalert(parent, theirs, recipient):
    '''
    Sends alerts to someone with a chore coming up the next day
    '''

    return 0

def main():
    '''
    Calls all parts of the update
    '''
    updatedb()
    sendalerts()

if __name__ == "__main__":
    main()
