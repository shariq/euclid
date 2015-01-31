#!/usr/bin/env python

import cPickle
import datetime
import threading
import time
import json
import random
import re
from bottle import route, hook, response, run, static_file

database = cPickle.load(open('../data/spring15.bin', 'rb'))


def updateInformation():
    weekday = datetime.datetime.now().weekday()
    time_later = (datetime.datetime.now() + datetime.timedelta(minutes = 15)).time()
    new_information = []
    for meeting in database:
        if meeting['weekday'] != weekday:
            continue
        if meeting['start'] < time_later < meeting['end']:
            new_meeting = meeting.copy()
            del new_meeting['start']
            del new_meeting['end']
            new_meeting['course'] = ', '.join(new_meeting['course'])
            new_information.append(new_meeting)
    if len(new_information) < 2:
        empty_meeting = {}
        empty_meeting['course'] = 'n/a'
        new_information.append(empty_meeting)
    globals()['information_string'] = json.dumps(new_information)
    globals()['information_list'] = map(json.dumps, new_information)

with open('index.html') as f:
    # this is absolutely horrible and we should use nginx
    globals()['index_html_content'] = f.read()

with open('index.css') as f:
    # this is absolutely horrible and we should use nginx
    globals()['index_css_content'] = f.read()

with open('index.js') as f:
    # this is absolutely horrible and we should use nginx
    globals()['index_js_content'] = f.read()

with open('quojs.js') as f:
    # this is absolutely horrible and we should use nginx
    globals()['quo_js_content'] = f.read()

def updateThread():
    while True:
        updateInformation()
        time.sleep(60)


updateInformation()
looper = threading.Thread(target = updateThread)
looper.daemon = True
looper.start()

@route('/')
def index():
    return static_file('index.html', root = '.')

@route('/index.css')
def index_css():
    return static_file('index.css', root = '.')

@route('/index.js')
def index_js():
    return static_file('index.js', root = '.')

@route('/quojs.js')
def index_js():
    return static_file('quojs.js', root = '.')

@route('/favicon.ico')
def index_js():
    return static_file('favicon.ico', root = '.')

@route('/all')
def all_data():
    return globals()['information_string']

@route('/random')
def select_data():
    return random.choice(globals()['information_list'])


run(host = '0.0.0.0', port = 80, server = 'tornado')
