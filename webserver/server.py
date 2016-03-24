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

@app.route('/')
def index():
    
#    # DEBUG: this is debugging code to see what request looks like
#    print request.method
#    print request.form
#    print request.args
    cursor = g.conn.execute("SELECT * FROM Person")
    output = list()
    for result in cursor:
        output.append(result)  # can also be accessed using result[0]
    cursor.close()
    return render_template("index.html", output=output)






DATABASEURI = "postgresql://jjg2188:GMRLGC@w4111db.eastus.cloudapp.azure.com/jjg2188"
engine = create_engine(DATABASEURI)

engine.execute("""DROP TABLE IF EXISTS Person;""")
engine.execute("""CREATE TABLE IF NOT EXISTS Person(
    user_id INT PRIMARY KEY,
    user_name CHAR(20),
    grad_date DATE,
    major_name CHAR(20)
    );""")
engine.execute("""INSERT INTO Person VALUES (1,'Jorge','2016-12-05','Computer Science');""")

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


