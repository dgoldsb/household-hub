"""
Author: Dylan Goldsborough
Date: February 2017
Description: main flask file for the super simple scheduler
"""

import os
import logging

from flask import Flask, render_template
import pyqrcode

from dbconn import fetch

app = Flask(__name__)
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
logging.basicConfig(
    filename=os.path.join(ROOT, "app.log"),
    filemode='a',
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)-8s %(thread)d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
LOG = logging.getLogger("app")


@app.route('/', methods=['GET'])
def start():
    """
    Shows the main page, with the main thing: the roster with chores so people do their fucking jobs.
    """
    LOG.info("Main page is requested.")
    planning = get_planning()
    return render_template('start.html', planning=planning)


def get_planning(only_now=False):
    """
    Gets the chore planning for the past two weeks, this week, and the next 5 weeks. The returned dictionary contains
    a header and a table. The header is a list, the table is a list of dictionaries.

    :param only_now: run for only the past two weeks (type=Boolean)
    :return: a table containing the planning (type=dict)
    """
    # Get a list of all chores in these weeks.
    with open(os.path.join(ROOT, "apps/templates/list_chores.sql"), 'r') as file:
        LOG.info("Fetching the planning with only_now = {}.".format(only_now))
        if only_now:
            job = file.read().format("-7", "+1")
        else:
            job = file.read().format("-14", "+37")
    columns = fetch(job)

    # Get the current week.
    current_week = fetch("SELECT DATE('now','weekday 0','-6 day')")[0][0]

    # Get a list of all dates in these weeks.
    with open(os.path.join(ROOT, "apps/templates/dates_in_week.sql"), 'r') as file:
        if only_now:
            job = file.read().format("-14", "+1")
        else:
            job = file.read().format("-14", "+37")
    rows = fetch(job)

    # Define some colors and the table.
    colors = ['#FFFFFF', '#D3D3D3']

    # Get the template job.
    with open(os.path.join(ROOT, "apps/templates/fetch_field.sql"), 'r') as file:
        template_job = file.read()

    # Build the table in a way that makes some sense.
    planning = []
    for row in rows:
        # Create a dictionary for the row.
        planning_row = dict()
        planning_row['values'] = []

        # Create a dictionary for the week.
        week_dict = dict()
        week_dict['value'] = row[0]
        week_dict['done'] = 2
        planning_row['values'].append(week_dict)

        # Loop over the columns.
        for column in columns:
            col = dict()
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
    result = dict()
    result['head'] = header
    result['table'] = planning

    return result


if __name__ == '__main__':
    host = '172.16.1.23'
    port = 1025

    # Create a QR code.
    address = '{}:{}'.format(host, port)
    filepath = os.path.join(ROOT, 'apps', 'static', 'qr.png')
    big_code = pyqrcode.create(address, error='M', version=27, mode='binary')
    big_code.png(filepath, scale=3, module_color='#000000', background='#ffffff')

    # Start the app.
    app.run(host=host, port=port, debug=True)
