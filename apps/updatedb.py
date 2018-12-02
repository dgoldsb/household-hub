"""
Update the database, weekly or daily cronjob.
"""

import logging
import os

from dbconn import execute, fetch_one, fetch

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
logging.basicConfig(filename=os.path.join(ROOT, 'hub.log'),
                    level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def truncate_database():
    """
    Truncates the database, and rebuilds.
    """
    # Truncate all weeks that did not happen yet.
    execute("DELETE FROM chorelog WHERE date_todo >= DATE('now','weekday 0')")


def update_database():
    """
    Add chores for the upcoming 10 weeks that have not been planned yet.
    """
    # Get the first weekday date last week.
    last_week = fetch_one("SELECT DATE('now','weekday 0','-6 day')")

    # Compile a list of dates.
    dates = []
    for i in range(0, 10):
        shift = i * 7 - 6
        if shift > 0:
            dates.append(fetch_one("SELECT DATE('now','weekday 0','+{} day')".format(shift)))
        else:
            dates.append(fetch_one("SELECT DATE('now','weekday 0','-{} day')".format(shift)))

    # Query all jobs and all the moments that the jobs were already scheduled.
    pairs_done = fetch("SELECT date_todo, CID FROM chorelog WHERE date_todo > DATE('now','weekday 0','-8 day')")
    jobs = fetch("SELECT DISTINCT CID FROM chores")

    # Create counting table.
    execute("INSERT INTO chores_unplanned SELECT UID, TID, CID, date_todo FROM chorelog WHERE date_todo > '{}'".format(
        last_week))

    # Iterate over the dates and jobs.
    for date in dates:
        if date is None:
            continue
        for chore in jobs:
            # Check if the job/date pair is done.
            if (date, chore[0]) not in pairs_done:
                # Determine the correct userID that should do the job.
                # Note that we order by no_jobs ASC, to give one job per person.
                query = """
                    SELECT a.UID
                           ,IFNULL(b.no_jobs,0) AS no_jobs
                           ,IFNULL(d.last_job,'2000-12-12') AS last_job
                           ,IFNULL(c.last_done,'2000-12-12') AS last_done
                    FROM    
                        (SELECT DISTINCT UID 
                        FROM housemate_chore
                        WHERE CID = {chore}) AS a 
                    LEFT JOIN 
                        (SELECT UID, count(CID) no_jobs 
                        FROM chores_unplanned 
                        WHERE date_todo = '{date}' AND UID IS NOT NULL 
                        GROUP BY UID) AS b 
                    ON a.UID = b.UID 
                    LEFT JOIN 
                        (SELECT UID, max(date_todo) AS last_done 
                            FROM chorelog 
                            WHERE CID = {chore} 
                            GROUP BY UID) AS c 
                    ON a.UID = c.UID 
                    LEFT JOIN (SELECT UID, max(date_todo) AS last_job 
                            FROM chorelog 
                            GROUP BY UID) AS d 
                    ON a.UID = d.UID
                    INNER JOIN (SELECT UID
                            FROM housemates
                            WHERE active = 1) as e
                    ON a.UID = e.UID
                    ORDER BY
                        no_jobs ASC
                       ,last_job ASC
                       ,last_done ASC""".format(chore=chore[0], date=date)
                assignee = fetch_one(query)
                
                # Update in the table that we use to count the number of jobs this week.
                execute("INSERT INTO chores_unplanned (UID, CID, date_todo) VALUES ({}, {}, '{}')".format(str(assignee),
                                                                                                          str(chore[0]),
                                                                                                          str(date)))

                # Insert into chorelog
                execute("INSERT INTO chorelog (date_todo, CID, finished, UID) VALUES ('{}', {}, 0, {})".format(str(date),
                                                                                                               str(chore[0]),
                                                                                                               str(assignee)))

    # Drop the counting table and commit database changes
    execute('DELETE FROM chores_unplanned')


if __name__ == '__main__':
    # Truncate (in case a person leaves or joins, make sure all weeks are recomputed).
    truncate_database()
    logging.info('Truncated database.')

    # Do the update.
    update_database()
    logging.info('Updated database.')
