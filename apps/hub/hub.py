"""
Author: Dylan Goldsborough
Date: February 2017
Description: main flask file for the compliance game
"""
from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for
from game import Game
import sys

app = Flask(__name__)
game_session = Game()

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        return redirect(url_for('adduser'))
    return render_template('start.html')

"""
First, let the user(s) enter their names (for highscore purposes)
"""
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        
        # Request: firstname, lastname
        firstname = request.form['fn']
        lastname = request.form['ln']

        if len(firstname) > 0 and len(lastname) > 0:
            game_session.add_groupmember(firstname, lastname)
        else:
            error = 'Input a name with non-zero length.'
            print(error, file = sys.stderr)
            return render_template('adduser.html', error = error)

        if request.form['add'] == "user":
            return render_template('adduser.html')
        if request.form['add'] == "group":
            return redirect(url_for('groupname'))
    if request.method == 'GET':
        return render_template('adduser.html')

"""
Second, let them enter a groupname
"""
@app.route('/groupname', methods=['POST', 'GET'])
def groupname():
    if request.method == 'POST':
        # Request: groupname
        groupname = request.form['groupname']

        if len(groupname) > 0 and len(groupname) < 250:
            # Check if uniques
            game_session.set_name(groupname)
        else:
            error = 'Input a group name between 1 and 250 characters.'
            return render_template('addgroup.html', error = error)
        return redirect(url_for('event'))
    if request.method == 'GET':
        return render_template('addgroup.html')

"""
Get into the event loop, it is the same page over and over with different
messages, prepared in the Python layer
"""
@app.route('/event', methods=['POST', 'GET'])
def event():
    if request.method == 'POST':
        next_event_id = request.form['action']
        game_session.goto_scenario(int(next_event_id))
        if int(next_event_id) == 999:
            return redirect(url_for('results'))
        return redirect(url_for('event'))
    if request.method == 'GET':
        scen_dict, options = game_session.get_scenario()
        print(scen_dict, file = sys.stderr)
        return render_template('room.html', groupname = game_session.get_name(), buttons = options
                               , scen_title = scen_dict['title'], scen_descr = scen_dict['story']
                               , multiple_choice = scen_dict['question_type'])

"""
Finish with a highscore screen, which should be able to refresh
"""
@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        # Do the query
        return render_template('results.html', groupname = game_session.get_name())
    if request.method == 'GET':
        game_session.submit_score()
        return render_template('results.html', groupname = game_session.get_name())

if __name__ == '__main__':
    app.run(debug=True)
