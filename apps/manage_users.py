"""
Add or deactivate users.
"""

import argparse

from dbconn import execute, fetch_one
from updatedb import truncate_database, update_database


def add_user(first_name, last_name, email=None):
    """
    Add a new active user.

    :param first_name: the first name of the user (full name as shown in the dashboard) (type=str)
    :param last_name: the last name of the user (full name as shown in the dashboard) (type=str)
    :param email: email of the user (type=str)
    """
    max_id = int(fetch_one('SELECT MAX(UID) FROM persons'))
    new_id = max_id + 1
    if email is not None:
        execute('INSERT INTO persons VALUES ({}, \'{}\', \'{}\', 1, \'{}\')'.format(new_id, first_name, last_name,
                                                                                    email))
    else:
        execute('INSERT INTO persons VALUES ({}, \'{}\', \'{}\', 1)'.format(new_id, first_name, last_name))
    truncate_database()
    update_database()


def deactivate_user(first_name, last_name):
    """
    Mark this user as deactivated.

    :param first_name: the first name of the user (full name as shown in the dashboard) (type=str)
    :param last_name: the last name of the user (full name as shown in the dashboard) (type=str)
    """
    execute('UPDATE persons SET active = 0 WHERE first_name = \'{}\' AND last_name = \'{}\''.format(first_name,
                                                                                                    last_name))
    truncate_database()
    update_database()


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--first_name', required=True, type=str, help='First name to add.')
    parser.add_argument('--last_name', required=True, type=str, help='Last name to add.')
    parser.add_argument('--email', required=False, default=None, type=str, help='Email address to add.')
    parser.add_argument('--action', required=True, type=str, help='Action to perform.')
    args = parser.parse_args()

    if args.action == 'add':
        add_user(args.first_name, args.last_name, args.email)
    elif args.action == 'deactivate':
        deactivate_user(args.first_name, args.last_name)
    else:
        raise ValueError('Unknown action {}.'.format(args.action))
