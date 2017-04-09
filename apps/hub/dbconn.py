'''
Module that handles database requests for the Flask layer
'''
from __future__ import print_function
import sqlite3
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..')

def flip_done(todo, chore):
    '''
    Flips the finished bit in the database
    '''
    args = (todo, chore)
    job = "UPDATE chorelog SET finished = CASE WHEN finished = 1 THEN 0 ELSE 1 END "\
          ", date_finished = DATE('now') WHERE date_todo = '%s'"\
          " AND CID = %s"
    insert(job, args)
    return 0

def get_offenders():
    '''
    Gets the housemates ordered by most non-done chores
    '''
    job = "SELECT a.first_name, IFNULL(b.no_chores,0) as no_chores FROM (SELECT first_name,"\
          " UID FROM housemates) as a "\
          "LEFT JOIN (SELECT UID, COUNT(*) as no_chores FROM chorelog "\
          "WHERE date_todo < DATE('now','weekday 0','-6 day') AND "\
          "finished = 0 GROUP BY UID) as b ON a.UID = b.UID "\
          "WHERE a.first_name <> 'None' "\
          "ORDER BY no_chores DESC" # +1 - 7 days, to give people one week to do a chore
    offenders = fetch(job)

    # Repackage: add headers
    header = ["Naam", "# keer niet gedaan"]
    result = {}
    result['head'] = header
    result['table'] = offenders

    return result

def get_planning(only_now=False):
    '''
    Gets the chore planning for the past two weeks, this week, and the next 5 weeks
    '''
    # Get a list of all chores in these weeks
    job = None
    if only_now:
        job = "SELECT DISTINCT a.CID, b.Chore FROM (SELECT * FROM chorelog "\
            "WHERE date_todo > DATE('now','weekday 0','-7 days') "\
            "AND date_todo < DATE('now','weekday 0','+1 days')) as a "\
            "LEFT JOIN (SELECT name as Chore, CID FROM chores) as b ON a.CID = b.CID"
    else:
        job = "SELECT DISTINCT a.CID, b.Chore FROM (SELECT * FROM chorelog "\
            "WHERE date_todo > DATE('now','weekday 0','-14 days') "\
            "AND date_todo < DATE('now','weekday 0','+37 days')) as a "\
            "LEFT JOIN (SELECT name as Chore, CID FROM chores) as b ON a.CID = b.CID"
    columns = fetch(job)

    thisweek = fetch("SELECT DATE('now','weekday 0','-6 day')")[0][0]

    # Get a list of all dates in these weeks
    if only_now:
        job = "SELECT DISTINCT date_todo FROM chorelog WHERE "\
            "date_todo > DATE('now','weekday 0','-14 days') "\
            "AND date_todo < DATE('now','weekday 0','+1 days')"
    else:
        job = "SELECT DISTINCT date_todo FROM chorelog WHERE "\
            "date_todo > DATE('now','weekday 0','-14 days') "\
            "AND date_todo < DATE('now','weekday 0','+37 days')"
    rows = fetch(job)

    # Build the table in a way that makes some sense
    # Define some colors and the table
    colors = ['#FFFFFF', '#D3D3D3']
    planning = []
    for row in rows:
        planning_row = {}
        planning_row['values'] = []
        week_dict = {}
        week_dict['value'] = row[0]
        week_dict['done'] = 2 # bit nonsense
        planning_row['values'].append(week_dict)
        for column in columns:
            col = {}
            args = (row[0], column[0])
            job = "SELECT a.first_name, b.finished, b.date_finished FROM "\
                  "(SELECT finished, date_finished, UID FROM chorelog WHERE "\
                  "date_todo = '%s' AND CID = %s) as b LEFT JOIN "\
                  "(SELECT first_name, UID FROM housemates) as a ON a.UID = B.UID"
            try:
                res = fetch(job, args)[0]
                col['value'] = res[0]
                col['when'] = res[2]
                col['done'] = res[1]
                col['CID'] = column[0]
                col['date'] = row[0]
                if col['value'] != 'None':
                    planning_row['values'].append(col)
            except:
                print('The date is not in the database', file=sys.stderr)

        print(row[0] == thisweek)
        print(thisweek)
        if row[0] == thisweek:
            planning_row['color'] = colors[1]
        else:
            planning_row['color'] = colors[0]

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
    conn = sqlite3.connect(os.path.join(ROOT, 'database/hub.db'))
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
    conn = sqlite3.connect(os.path.join(ROOT, 'database/hub.db'))
    conn.text_factory = str
    curs = conn.cursor()
    if args is not None:
        curs.execute(job % args)
    else:
        curs.execute(job)
    table = curs.fetchall()
    return table

