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
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
DATABASEURI = "sqlite:///test.db"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
    id serial,
    name text
    );""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")

#engine.execute("""DROP TABLE IF EXISTS Person;""")
#engine.execute("""CREATE TABLE IF NOT EXISTS Person(
#    user_id INT PRIMARY KEY,
#    user_name CHAR(100),
#    grad_date DATE,
#    major_name CHAR(100)
#    );""")
#engine.execute("""INSERT INTO test VALUES (1,Jorge,05 Dec 2016,Computer Science);""")


#engine.execute("""DROP TABLE IF EXISTS University;""")
#engine.execute("""create TABLE University(
#    univ_id int,
#    univ_name text,
#    Primary key(univ_id)
#    );""")
#
#engine.execute("""DROP TABLE IF EXISTS Courses;""")
#engine.execute("""create TABLE Courses(
#    course_id int,
#    course_name text,
#    course_description text,
#    Primary key(course_id)
#    );""")
#
#engine.execute("""DROP TABLE IF EXISTS Enrollment;""")
#engine.execute("""create TABLE Enrollment(
#    univ_id int,
#    user_id int,
#    course_id int,
#    Primary key(user_id, univ_id, course_id),
#    Foreign key(user_id) references Person ON DELETE CASCADE,
#    Foreign key(univ_id) references University ON DELETE CASCADE,
#    Foreign key(course_id) references Courses ON DELETE CASCADE
#    );""")
#
#engine.execute("""DROP TABLE IF EXISTS Company;""")
#engine.execute("""create TABLE Company(
#    company_id int,
#    company_name text,
#    Primary key(company_id)
#    );""")
#
#engine.execute("""DROP TABLE IF EXISTS Jobs;""")
#engine.execute("""create TABLE Jobs(
#    job_id int,
#    job_name text,
#    job_type int,
#    job_description text,
#    Primary key(job_id)
#    );""")
#
#engine.execute("""DROP TABLE IF EXISTS Employed;""")
#engine.execute("""create Table Employed(
#    user_id int,
#    company_id int,
#    job_id int,
#    Primary key(user_id),
#    Foreign key(user_id) references Person ON DELETE CASCADE,
#    Foreign key(company_id) references Company ON DELETE CASCADE,
#    Foreign key(job_id) references Jobs ON DELETE CASCADE
#    );""")
#
#
#
#engine.execute("""DROP TABLE IF EXISTS Skills;""")
#engine.execute("""create Table Skills(
#    skill_id int,
#    skill_name text,
#    Primary key(skill_id)
#
#    );""")
#
#engine.execute("""DROP TABLE IF EXISTS Vacant;""")
#engine.execute("""create Table Vacant(
#    job_id int,
#    company_id int,
#    Primary key(job_id, company_id),
#    Foreign key(job_id) references Jobs ON DELETE CASCADE,
#    Foreign key(company_id) references Company ON DELETE CASCADE
#    );""")
#
#engine.execute("""DROP TABLE IF EXISTS Possesses;""")
#engine.execute("""create Table Possesses(
#    skill_id int,
#    user_id int,
#    endorsements int,
#    skill_level text,
#    Primary key(skill_id, user_id),
#    Foreign key(skill_id) references Skills ON DELETE CASCADE,
#    Foreign key(user_id) references Person ON DELETE CASCADE
#    );""")
#
#engine.execute("""DROP TABLE IF EXISTS Endorses;""")
#engine.execute("""create table Endorses(
#    user_id_src int,
#    user_id_dest int,
#    skill_id int,
#    Primary Key(skill_id, user_id_src, user_id_dest),
#    Foreign key(skill_id) references Skills ON DELETE CASCADE,
#    Foreign key(user_id_src) references Person(user_id) ON DELETE CASCADE,
#    Foreign Key(user_id_src) references Person(user_id) ON DELETE CASCADE
#    );""")
#
#engine.execute("""DROP TABLE IF EXISTS Requires;""")
#engine.execute("""create Table Requires(
#    job_id int,
#    skill_id int,
#    Primary Key(job_id, skill_id),
#    Foreign Key(job_id) references Jobs ON DELETE CASCADE,
#    Foreign Key(skill_id) references Skills ON DELETE CASCADE
#    );""")
#
# END SQLITE SETUP CODE



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
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
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
  print request.args


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/another')
def another():
  return render_template("anotherfile.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


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
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
