from collections import defaultdict
import json
import os
import sqlite3
import uuid

from flask import g, session

from HackerHats import app


def add_response(case_id, response, user_id=None):
    if user_id == None:
        user_id = get_uuid();
    db = get_db()
    db.execute('replace into responses (user_id, case_id, response) values (?, ?, ?)',
                 (user_id, case_id, response))
    db.commit()
    
def get_all_responses():
    response_rows = query_db('select case_id, response from responses')
    
    responses = defaultdict(list)
    for response in response_rows:
        responses[response['case_id']].append(dict(response))
    return responses

def get_user_response(case_id, user_id=None):
    if user_id == None:
        user_id = get_uuid();
    res = query_db("select response from responses where case_id = ? and user_id = ?", (case_id, user_id), True);
    if res != None:
        return res["response"]
    else:
        return None

def get_responses(case_id):
    return query_db('select response from responses where case_id = ?', (case_id,))

def get_all_cases():
    return query_db('select * from cases')

def get_case(case_id):
    return query_db('select * from cases where id = ?', (case_id,), True)

def get_case_ids():
    case_ids = query_db('select id from cases order by id')
    return [case_id['id'] for case_id in case_ids]

def get_uuid():
    if 'uuid' in session:
        return session['uuid']
    else:
        session.permanent = True
        u = str(uuid.uuid4())
        session['uuid'] = u
        return u

# Database exceptions

@app.errorhandler(sqlite3.IntegrityError)
def integrity_error_handler(error):
    return "This request tried to break the database integrity!", 400

# Database boilerplate

def connect_db():
    """Connects to the database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    rv.execute('pragma foreign_keys = on')
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
def init_db():
    db = get_db()
    with app.open_resource(os.path.join(app.root_path, 'db' 'data.db'), mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
