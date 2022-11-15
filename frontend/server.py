#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver
To run locally
    python server.py
Go to http://localhost:8111 in your browser
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from os import abort
# from turtle import home
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from icecream import ic
import auth
import home
from auth import *
from home import *
import functions
from functions import *
import userpage
from userpage import *
import help
from help import *

# from db_utils import get_db_conn

tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'templates')
ic(tmpl_dir)
app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_mapping(SECRET_KEY='xysong')
app.register_blueprint(auth.bp)
app.register_blueprint(home.bp)
app.register_blueprint(functions.bp)
app.register_blueprint(userpage.bp)
app.register_blueprint(help.bp)

# XXX: The Database URI should be in the format of:
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/<DB_NAME>
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# For your convenience, we already set it to the class database

# Use the DB credentials you received by e-mail
DB_USER = 'xs2485'
DB_PASSWORD = "Sxy20000425"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DB_SERVER2 = "w4111project1part2db.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":" + \
    DB_PASSWORD+"@"+DB_SERVER2+"/proj1part2"
# local_database = "postgresql://postgres:Sxy20000425@localhost/proj1part3"
# engine = create_engine(local_database)

# engine = get_db_conn()
#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request
    The variable g is globally accessible
    """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
    """
    request is a special object that Flask provides to access web request information:
    request.method:   "GET" or "POST"
    request.form:     if the browser submitted a form, this contains the data in the form
    request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2
    See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
    """

    # DEBUG: this is debugging code to see what request looks like
    print(request.args)

    #
    return render_template("index.html")

#
# This is an example of a different path.  You can see it at
#
#     localhost:8111/another
#
# notice that the function name is another() rather than index()
# the functions for each app.route needs to have different names
#


@app.route('/another')
def another():
    return render_template("anotherfile.html")


# @app.route('/example')
# def example():
#     ex = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
#     cursor = g.conn.execute(ex)
#     data = [row for row in cursor]
#     return render_template("example.html", data=data)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    print(name)
    cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)'
    g.conn.execute(text(cmd), name1=name, name2=name)
    return redirect('/')


if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using
            python server.py
        Show the help text using
            python server.py --help
        """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
