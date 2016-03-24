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

DATABASEURI = "postgresql://jjg2188:GMRLGC@w4111db.eastus.cloudapp.azure.com/jjg2188"
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


engine.execute("""DROP TABLE IF EXISTS Person CASCADE;""")
engine.execute("""CREATE TABLE IF NOT EXISTS Person(
    user_id INT PRIMARY KEY,
    user_name CHAR(20),
    grad_date DATE,
    major_name CHAR(20)
    );""")

person_values = [('1','Jorge','2016-12-05','Computer Science'),
                 ('2','Tulika','2016-12-05','Computer Science'),
                 ('3','Laura','2015-08-15','Computer Science'),
                 ('4','Evan','2017-05-20','Computer Science'),
                 ('5','John','2014-05-21','Computer Science'),
                 ('6','Michael','2018-12-7','Computer Science'),
                 ('7','Christina','2018-12-12','Computer Science'),
                 ('8','Jennifer','2017-08-15','Computer Science'),
                 ('9','Karla','2016-08-03','Computer Science'),
                 ('10','Gina','2019-05-012','Computer Science')]
for pv in person_values:
    engine.execute("INSERT INTO Person(user_id, user_name, grad_date, major_name) VALUES (%s,%s,%s,%s)",pv)

engine.execute("""DROP TABLE IF EXISTS University CASCADE;""")
engine.execute("""create TABLE University(
    univ_id int,
    univ_name text,
    Primary key(univ_id)
    );""")

university_values = [('1', 'Columbia University'),
                     ('2', 'University of Central Florida'),
                     ('3', 'New York University'),
                     ('4', 'Cornell University'),
                     ('5', 'Oxford University'),
                     ('6', 'Georgia Institute of Technology'),
                     ('7', 'Harvard University'),
                     ('8', 'Massachusetts Institute of Technology'),
                     ('9', 'IMB'),
                     ('10', 'Goldman Sach')]

for uv in university_values:
    engine.execute("INSERT INTO University (univ_id, univ_name) VALUES (%s,%s)",uv)

engine.execute("""DROP TABLE IF EXISTS Company CASCADE;""")
engine.execute("""create TABLE Company(
    company_id int,
    company_name text,
    Primary key(company_id)
    );""")

company_values = [('1', 'Intel Co.'),
                     ('2', 'Google'),
                     ('3', 'Facebook'),
                     ('4', 'Microsoft'),
                     ('5', 'Oracle'),
                     ('6', 'SpaceX'),
                     ('7', 'Tesla'),
                     ('8', 'Twitter'),
                     ('9', 'Stanford University'),
                     ('10', 'Carnegie Mellon University')]
for cv in company_values:
    engine.execute("INSERT INTO Company (company_id, company_name) VALUES (%s,%s)",cv)

engine.execute("""DROP TABLE IF EXISTS Skills CASCADE;""")
engine.execute("""create Table Skills(
    skill_id int,
    skill_name text,
    Primary key(skill_id)

    );""")

skills_values = [('1', 'Python'),
                  ('2', 'Java'),
                  ('3', 'C++'),
                  ('4', 'R'),
                  ('5', 'Matlab'),
                  ('6', 'C#'),
                  ('7', 'SQL'),
                  ('8', 'Perl'),
                  ('9', 'BASIC'),
                  ('10', 'Excel')]

for sv in skills_values:
    engine.execute("INSERT INTO Skills (skill_id, skill_name) VALUES (%s,%s)",sv)

engine.execute("""DROP TABLE IF EXISTS Courses CASCADE;""")
engine.execute("""create TABLE Courses(
    course_id int,
    course_name text,
    course_description text,
    Primary key(course_id)
    );""")

course_values = [('4777', 'Machine Learning', 'Teaching machines how to learn'),
                 ('4111', 'Intro to Databases', 'Database analysis'),
                 ('4204', 'Probabilities and Statistics', 'Probablity Theory'),
                 ('4334', 'Data Mining', 'Statistical Analysis'),
                 ('4889', 'Big Data', 'How to handle big data'),
                 ('4034', 'Computational Learning Theory', 'Analysis of ML theory'),
                 ('4049', 'Linear Algebra', 'Mathematical concepts of Matrices'),
                 ('4564', 'NLP', 'Processing of natural language'),
                 ('4903', 'PLT', 'Development of programming languages'),
                 ('4667', 'Operating Systems', 'Understanding of OS')]

for cv in course_values:
    engine.execute("INSERT INTO Courses (course_id, course_name,course_description) VALUES (%s,%s,%s)",cv)


engine.execute("""DROP TABLE IF EXISTS Enrollment CASCADE;""")
engine.execute("""create TABLE Enrollment(
    univ_id int,
    user_id int,
    course_id int,
    Primary key(user_id, univ_id, course_id),
    Foreign key(user_id) references Person ON DELETE CASCADE,
    Foreign key(univ_id) references University ON DELETE CASCADE,
    Foreign key(course_id) references Courses ON DELETE CASCADE
    );""")

enrollment_values = [('1','3','4777'),
                     ('2','1','4034'),
                     ('1','3','4889'),
                     ('2','1','4889'),
                     ('2','1','4777'),
                     ('2','2','4777'),
                     ('2','2','4889'),
                     ('7','2','4889'),
                     ('8','9','4777'),
                     ('8','9','4889'),
                     ('6','4','4889'),
                     ('6','4','4777'),
                     ('6','4','4034'),
                     ('5','7','4889'),
                     ('5','7','4334'),
                     ('3','4','4777'),
                     ('10','10','4334'),
                     ('10','10','4889'),
                     ('10','10','4777'),
                     ('9','8','4034'),
                     ('9','8','4334'),
                     ('9','8','4667')]
for ev in enrollment_values:
    engine.execute("INSERT INTO Enrollment (univ_id, user_id,course_id) VALUES (%s,%s,%s)",ev)

engine.execute("""DROP TABLE IF EXISTS Jobs CASCADE;""")
engine.execute("""create TABLE Jobs(
    job_id int,
    job_name text,
    job_type text,
    job_description text,
    Primary key(job_id)
    );""")

jobs_values = [('1','Programmer','Intern','Program writter'),
               ('2','Elecrical Engineering','Full Time','Device Physics Designer'),
               ('3','Web Developer','Part Time','Web development and interface'),
               ('4','Bussiness Rep','Full Time','Create relationships'),
               ('5','CEO','Full Time','Run company'),
               ('6','Statistician Marker','Intern','Analysis of Market data'),
               ('7','DC Engineer','Full Time','DC designer'),
               ('8','Android Developer','Part Time','mobile OS app developmer'),
               ('9','Window Security Staff','Part Time','encryption'),
               ('10','Secretary','Part Time','help!')]

for jv in jobs_values:
    engine.execute("INSERT INTO Jobs (job_id, job_name,job_type,job_description) VALUES (%s,%s,%s,%s)",jv)

engine.execute("""DROP TABLE IF EXISTS Vacant CASCADE;""")
engine.execute("""create Table Vacant(
    job_id int,
    company_id int,
    Primary key(job_id, company_id),
    Foreign key(job_id) references Jobs ON DELETE CASCADE,
    Foreign key(company_id) references Company ON DELETE CASCADE
    );""")

vacant_values = [ ('3','4'),
                  ('5','6'),
                  ('7','7'),
                  ('8','3'),
                  ('1','1'),
                  ('2','2'),
                  ('3','3'),
                  ('4','1'),
                  ('4','5'),
                  ('5','3'),
                  ('5','5'),
                  ('10','1')]

for vv in vacant_values:
    engine.execute("INSERT INTO Vacant (job_id, company_id) VALUES (%s,%s)",vv)


engine.execute("""DROP TABLE IF EXISTS Possesses CASCADE;""")
engine.execute("""create Table Possesses(
    skill_id int,
    user_id int,
    endorsements int,
    skill_level text,
    Primary key(skill_id, user_id),
    Foreign key(skill_id) references Skills ON DELETE CASCADE,
    Foreign key(user_id) references Person ON DELETE CASCADE
    );""")

possesses_values = [('1','3','2','Proficient'),
                    ('2','4','1','Advanced'),
                    ('4','2','5','Intermediate'),
                    ('3','2','3','Proficient'),
                    ('5','2','1','Advanced'),
                    ('6','2','3','Proficient'),
                    ('1','1','3','Basic'),
                    ('2','1','4','Intermediate'),
                    ('5','1','3','Proficient'),
                    ('6','10','3','Proficient'),
                    ('5','3','4','Advanced')]

for pv in possesses_values:
    engine.execute("INSERT INTO Possesses (skill_id, user_id, endorsements, skill_level) VALUES (%s,%s,%s,%s)",pv)

engine.execute("""DROP TABLE IF EXISTS Endorses CASCADE;""")
engine.execute("""create table Endorses(
    user_id_src int,
    user_id_dest int,
    skill_id int,
    Primary Key(skill_id, user_id_src, user_id_dest),
    Foreign key(skill_id) references Skills ON DELETE CASCADE,
    Foreign key(user_id_src) references Person(user_id) ON DELETE CASCADE,
    Foreign Key(user_id_src) references Person(user_id) ON DELETE CASCADE
    );""")

endorses_values = [('2','3','1'),
                   ('4','3','1'),
                   ('5','3','5'),
                   ('6','3','5'),
                   ('7','3','5'),
                   ('9','3','5'),
                   ('4','1','1'),
                   ('3','1','1'),
                   ('2','1','1'),
                   ('6','1','2'),
                   ('7','1','2'),
                   ('3','1','2'),
                   ('2','1','2'),
                   ('5','1','5'),
                   ('2','1','5'),
                   ('9','1','5'),
                   ('7','10','6'),
                   ('8','10','6'),
                   ('3','10','6'),
                   ('2','4','2'),
                   ('4','2','4'),
                   ('3','2','4'),
                   ('7','2','4'),
                   ('8','2','4'),
                   ('10','2','4'),
                   ('7','2','3'),
                   ('8','2','3'),
                   ('1','2','3'),
                   ('3','2','5'),
                   ('10','2','6'),
                   ('9','2','6'),
                   ('8','2','6')]

for ev in endorses_values:
    engine.execute("INSERT INTO Endorses (user_id_src, user_id_dest,skill_id) VALUES (%s,%s,%s)",ev)

engine.execute("""DROP TABLE IF EXISTS Requires CASCADE;""")
engine.execute("""create Table Requires(
    job_id int,
    skill_id int,
    Primary Key(job_id, skill_id),
    Foreign Key(job_id) references Jobs ON DELETE CASCADE,
    Foreign Key(skill_id) references Skills ON DELETE CASCADE
    );""")

requires_values = [('2','4'),
                   ('4','4'),
                   ('2','3'),
                   ('6','7'),
                   ('4','5'),
                   ('1','2'),
                   ('1','3'),
                   ('5','5'),
                   ('7','8'),
                   ('2','8'),
                   ('9','1'),
                   ('10','1'),
                   ('10','2'),
                   ('10','3'),
                   ('10','4')]
for rv in requires_values:
    engine.execute("INSERT INTO Requires (job_id, skill_id) VALUES (%s,%s)",rv)


engine.execute("""DROP TABLE IF EXISTS Employed CASCADE;""")
engine.execute("""create Table Employed(
    user_id int,
    company_id int,
    job_id int,
    Primary key(user_id),
    Foreign key(user_id) references Person ON DELETE CASCADE,
    Foreign key(company_id) references Company ON DELETE CASCADE,
    Foreign key(job_id) references Jobs ON DELETE CASCADE
    );""")

employed_values = [('8','9','2'),
                   ('6','4','8'),
                   ('5','7','4'),
                   ('3','4','7'),
                   ('10','10','8'),
                   ('9','8','9'),
                   ('1','5','7'),
                   ('2','4','2')]

for ev in employed_values:
    engine.execute("INSERT INTO Employed (user_id, company_id, job_id) VALUES (%s,%s, %s)",ev)



@app.route('/')
def index():
    
    #    # DEBUG: this is debugging code to see what request looks like
    #    print request.method
    #    print request.form
    #    print request.args
    
    #   query
    cursor = g.conn.execute("SELECT user_name FROM Person")
    output = list()
    for result in cursor:
        output.append(result)  # can also be accessed using result[0]
    cursor.close()


#    cursor = g.conn.execute("SELECT University.univ_id, University.univ_name, COUNT(*) maximum FROM University INNER JOIN Enrollment ON Enrollment.univ_id = University.univ_id GROUP BY University.univ_id ORDER BY maximum DESC LIMIT 1;")

    cursor = g.conn.execute("SELECT Person.user_name FROM Person WHERE Person.user_id IN (Select Enrollment.user_id FROM Enrollment WHERE univ_id = 2 and course_id = 4777);")

#    cursor = g.conn.execute("SELECT Jobs.job_id, Jobs.job_name FROM Jobs WHERE job_id IN (SELECT Vacant.job_id FROM Vacant, Requires WHERE Vacant.job_id = Requires.job_id and (skill_id = 1 or skill_id =2));")

    
    record = cursor.fetchone()
    cursor.close()
    return render_template("index.html", output=record)


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


