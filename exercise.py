#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for
from os import _exit
from os.path import exists
from sqlite3 import connect
import re

if not exists('database.sqlite3'):
    print('[x] Database does not exist; run createdb.py first.\n\nExiting...')
    _exit(1)

app = Flask('exercise 1')

logged_in = False

def validate(user_name, password):
	#This is to check if username has any special charactor or not 
	regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
	print(len(user_name))
	print(len(password))
	if(len(user_name) == 0 or len(password) == 0):
		return False
	else:
		if(regex.search(user_name) == None):
			return True 
		else:
			return False
	
def get_index_page(user_name):
	print(user_name)
	if(user_name == 'admin'):
		return 'index'
	else:
		return 'user.html'
		
@app.route('/', methods=['GET'])
def index():
    if logged_in:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in
    if logged_in:
        return redirect(url_for('index'))
    if request.method == 'POST':
        conn = connect('database.sqlite3')
        db_cursor = conn.cursor()
        user_name = request.form['username']
        password = request.form['password']
        validated = validate(user_name, password)
        print(validated)
        if(validated):
        	success = len([row for row in db_cursor.execute('''SELECT * FROM users WHERE
                                                           username = "%s" AND password = "%s"''' %
                                                           (request.form['username'], request.form['password']))]) == 1
        else:
        	success = False                                                   
        conn.close()
        if success:
            logged_in = True
            print(get_index_page(user_name))
            return redirect(url_for('index'))
        else:
            return render_template('login.html', login_failed=True)

    return render_template('login.html')


if __name__ == '__main__':
    app.run(port='8080')
