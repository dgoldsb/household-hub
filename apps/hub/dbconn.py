'''
Module that handles database requests for the Flask layer
'''
from __future__ import print_function
import sqlite3

def get_offenders():
    '''
    Gets the housemates ordered by most non-done chores
    '''
    job = "SELECT a.first_name, IFNULL(b.no_chores,0) FROM (SELECT first_name,"\
          " UID FROM housemates) as a "\
          "LEFT JOIN (SELECT UID, COUNT(*) as no_chores FROM chorelog "\
          "WHERE date_todo < DATE('now') AND finished = 0 GROUP BY UID) as b ON a.UID = b.UID"
    offenders = fetch(job)

    # Repackage: add headers
    header = ["Naam", "# keer niet gedaan"]
    result = {}
    result['head'] = header
    result['table'] = offenders

    return result

def get_planning():
    '''
    Gets the chore planning for the past two weeks, this week, and the next 5 weeks
    '''
    # Get a list of all chores in these weeks
    job = "SELECT DISTINCT a.CID, b.Chore FROM (SELECT * FROM chorelog "\
          "WHERE date_todo > DATE('now','weekday 0','-15 days') "\
          "AND date_todo < DATE('now','weekday 0','35 days')) as a "\
          "LEFT JOIN (SELECT name as Chore, CID FROM chores) as b ON a.CID = b.CID"
    columns = fetch(job)

    # Get a list of all dates in these weeks
    job = "SELECT DISTINCT date_todo FROM chorelog WHERE "\
          "date_todo > DATE('now','weekday 0','-15 days') "\
          "AND date_todo < DATE('now','weekday 0','35 days')"
    rows = fetch(job)

    # Build the table in a way that makes some sense
    # Define some colors and the table
    colors = ['#ccff33', '#66ff66', '#cc66ff']
    planning = []
    for row in rows:
        planning_row = {}
        planning_row['values'] = []
        week_dict = {}
        week_dict['value'] = row[0]
        print(row[0])
        week_dict['done'] = 0 # bit nonsense
        planning_row['values'].append(week_dict)
        for column in columns:
            col = {}
            args = (row[0], column[0])
            job = "SELECT a.first_name, b.finished, b.date_finished FROM "\
                  "(SELECT finished, date_finished, UID FROM chorelog WHERE "\
                  "date_todo = '%s' AND CID = %s) as b LEFT JOIN "\
                  "(SELECT first_name, UID FROM housemates) as a ON a.UID = B.UID"
            res = fetch(job, args)[0]
            col['value'] = res[0]
            col['when'] = res[2]
            col['done'] = res[1]
            planning_row['values'].append(col)
        planning_row['color'] = colors[0] # TODO: change this
        planning.append(planning_row)

    # Repackage: add headers and colors
    header = ['Week']
    for column in columns:
        header.append(column[1])

    result = {}
    result['head'] = header
    result['table'] = planning
    return result

def insert(job, args=None):
    '''
    Parameter job is the c-style substitution string, args is tuple
    '''
    conn = sqlite3.connect('../../hub.db')
    conn.text_factory = str
    curs = conn.cursor()
    if args is not None:
        curs.execute(job % args)
    else:
        curs.execute(job)
    conn.commit()
    return 0

def fetch(job, args=None):
    '''
    Gets and returns a table from the database
    Always returns a fetchall (tuples in list), so a single element is [0][0]
    '''
    conn = sqlite3.connect('../../hub.db')
    conn.text_factory = str
    curs = conn.cursor()
    if args is not None:
        curs.execute(job % args)
    else:
        curs.execute(job)
    table = curs.fetchall()
    return table
