"""
Module that handles database requests for the Flask layer.
"""

import logging
import os
import sqlite3

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..')
DATABASE = os.path.join(ROOT, 'database/hub.db')
logging.basicConfig(
    filename=os.path.join(ROOT, "dbconn.log"),
    filemode='a',
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)-8s %(thread)d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
LOG = logging.getLogger("dbconn")


def flip_done(todo, chore):
    """
    Flips the finished bit in the database.
    
    :param todo: the date on which the chore is to be flipped
    :param chore: the chore for which to flip
    :return True if something was flipped
    """
    args = (todo, chore)
    with open(os.path.join(ROOT, "templates/flip.sql"), 'r') as file:
        job = file.read()
    try:
        LOG.info("Flipping the done tag for {} on {}.".format(chore, todo))
        insert(job, args)
        return True
    except ValueError as e:
        LOG.error(e)
        return False


def get_offenders():
    """
    Gets the person ordered by most non-done chores.

    :return a table of the persons ordered by numbers of time not done in time
    """
    with open(os.path.join(ROOT, "templates/offenders.sql"), 'r') as file:
        job = file.read()
    offenders = fetch(job)

    # Repackage: add header and a table.
    header = ["Name", "Times not done"]
    result = {}
    result['head'] = header
    result['table'] = offenders
    return result


def get_planning(only_now=False):
    """
    Gets the chore planning for the past two weeks, this week, and the next 5 weeks.

    :param only_now: run for only the past two weeks.
    :return: a table containing the planning
    """
    # Get a list of all chores in these weeks.
    with open(os.path.join(ROOT, "templates/list_chores.sql"), 'r') as file:
        LOG.info("Fetching the planning with only_now = {}.".format(only_now))
        if only_now:
            job = file.read().format("-7", "+1")
        else:
            job = file.read().format("-14", "+37")
    columns = fetch(job)

    # Get the current week.
    current_week = fetch("SELECT DATE('now','weekday 0','-6 day')")[0][0]

    # Get a list of all dates in these weeks.
    with open(os.path.join(ROOT, "templates/dates_in_week.sql"), 'r') as file:
        if only_now:
            job = file.read().format("-14", "+1")
        else:
            job = file.read().format("-14", "+37")
    rows = fetch(job)

    # Define some colors and the table.
    colors = ['#FFFFFF', '#D3D3D3']

    # Get the template job.
    with open(os.path.join(ROOT, "templates/fetch_field.sql"), 'r') as file:
        template_job = file.read()

    # Build the table in a way that makes some sense.
    planning = []
    for row in rows:
        # Create a dictionary for the row.
        planning_row = {}
        planning_row['values'] = []

        # Create a dictionary for the week.
        week_dict = {}
        week_dict['value'] = row[0]
        week_dict['done'] = 2
        planning_row['values'].append(week_dict)

        # Loop over the columns.
        for column in columns:
            col = {}
            args = (row[0], column[0])
            try:
                res = fetch(template_job, args)[0]
                col['value'] = res[0]
                col['when'] = res[2]
                col['done'] = res[1]
                col['CID'] = column[0]
                col['date'] = row[0]
                if col['value'] != 'None':
                    planning_row['values'].append(col)
            except ValueError as e:
                LOG.error(e)

        # We highlight the current week.
        if row[0] == current_week:
            planning_row['color'] = colors[1]
        else:
            planning_row['color'] = colors[0]

        # We add the row to our table.
        planning.append(planning_row)

    # Repackage: add headers and colors.
    header = ['Week']
    for column in columns:
        header.append(column[1])
    result = {}
    result['head'] = header
    result['table'] = planning
    return result


def insert(job, args=None):
    """
    Parameter job is the c-style substitution string, args is tuple.
    
    :param job: a query to run
    :param args: arguments for the query, will be placed on the '?'
    """
    conn = sqlite3.connect(DATABASE)
    conn.text_factory = str
    curs = conn.cursor()
    if args is not None:
        curs.execute(job % args)
    else:
        curs.execute(job)
    conn.commit()


def fetch(job, args=None):
    """
    Gets and returns a table from the database
    Always returns a fetchall (tuples in list), so a single element is [0][0].
    
    :param job: a query to run
    :param args: arguments for the query, will be placed on the '?'
    :return: fetched data
    """
    conn = sqlite3.connect(DATABASE)
    conn.text_factory = str
    curs = conn.cursor()
    if args is not None:
        curs.execute(job % args)
    else:
        curs.execute(job)
    table = curs.fetchall()
    return table
