"""
Module that handles database requests for the Flask layer.
"""

import os
import sqlite3

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..')
DATABASE = os.path.join(ROOT, 'database/hub.db')


def execute(job, args=None):
    """
    Parameter job is the c-style substitution string, args is tuple.
    
    :param job: a query to run (type=str)
    :param args: arguments for the query, will be placed on the '?' (type=tuple)
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
    Gets and returns a table from the database.
    Always returns a fetchall (tuples in list), so a single element is [0][0].
    
    :param job: a query to run (type=str)
    :param args: arguments for the query, will be placed on the '?' (type=tuple)
    :return: fetched data (type=list(list))
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


def fetch_one(job, args=None):
    """
    Gets and returns a table from the database. Returns a fetchone[0].

    :param job: a query to run (type=str)
    :param args: arguments for the query, will be placed on the '?' (type=tuple)
    :return: fetched data (type=str)
    """
    conn = sqlite3.connect(DATABASE)
    conn.text_factory = str
    curs = conn.cursor()
    if args is not None:
        curs.execute(job % args)
    else:
        curs.execute(job)
    value = curs.fetchone()[0]
    return value
