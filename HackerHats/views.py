import os

from flask import Flask, session, request
import flask

from HackerHats import app
from HackerHats import database
import bisect
from werkzeug.exceptions import NotFound


# Pages
@app.route('/')
def root():
    return definitions()

@app.route('/definitions')
def definitions():
    return flask.render_template('definitions.jinja2',
                                 next_page=flask.url_for('case', case_id=database.get_case_ids()[0]))
    
@app.route('/case/<int:case_id>')
def case(case_id):
    case = database.get_case(case_id)
    if case != None:
        case_ids, i = case_id_index(case_id)
        params = {}
        params['next_page'] = flask.url_for('results', case_id=case_id)
        if (i - 1) >= 0:
            params['prev_page'] = flask.url_for('results', case_id=case_ids[i - 1])
        else:
            params['prev_page'] = '/definitions'
        params['case'] = dict(case)
        
        # Preselect existing response, if any
        default_response = database.get_user_response(case_id)
        if default_response != None:
            params['default_response'] = default_response

        # Show instruction overlay if it has not been shown before
        if not 'case_overlay' in session:
            params['has_overlay'] = True;
            session['case_overlay'] = True;

        return flask.render_template('case.jinja2', **params)
    else:
        raise NotFound

@app.route('/results/<int:case_id>')
def results(case_id):
    case = database.get_case(case_id)
    if case != None:
        case_ids, i = case_id_index(case_id)
        params = {}
        if (i + 1) < len(case_ids):
            params['next_page'] = flask.url_for('case', case_id=case_ids[i + 1])
        params['prev_page'] = flask.url_for('case', case_id=case_id)
        params['case'] = case
        params['responses'] = [dict(response) for response in database.get_responses(case_id)]
        # Show instruction overlay if it has not been shown before
        if not 'response_overlay' in session:
            params['has_overlay'] = True;
            session['response_overlay'] = True;
        return flask.render_template('results.jinja2', **params)
    else:
        raise NotFound

@app.route('/words')
def words():
    cases = database.get_all_cases()
    word_count = sum([len(case[s].split()) for s in ['body', 'title', 'details'] for case in cases])
    return flask.render_template('words.jinja2', word_count=word_count)

@app.route('/about')
def about():
    return flask.render_template('about.jinja2')

@app.route('/favicon.ico')
def favicon():
    return send_static('img/favicons/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<path:path>')
def send_static(path, **options):
    return flask.send_from_directory(os.path.join(app.root_path, 'static'), path, **options)

@app.route('/responses/submit', methods=['POST'])
def submit_response():
    res = request.form['response'].lower()
    if res == "black" or res == "gray" or res == "white":
        database.add_response(request.form['case_id'], res)
        return "Success!"
    else:
        return "Invalid response: %s" % res, 400

@app.errorhandler(404)
def error(e):
    return flask.render_template('error.jinja2', message="The page you requested does not exist."), 404

def case_id_index(case_id):
    case_ids = database.get_case_ids()
    i = bisect.bisect_left(case_ids, case_id)
    if i != len(case_ids) and case_ids[i] == case_id:
        return case_ids, i
    raise ValueError
