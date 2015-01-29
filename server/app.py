#!/usr/bin/env python

import cPickle
import datetime
import threading
import time
import json
import re
from bottle import route, hook, response, run, static_file

database = cPickle.load(open('../data/spring15.bin', 'rb'))

globals()['information'] = ''


def updateInformation():
    weekday = datetime.datetime.now().weekday()
    time_now = datetime.datetime.now().time()
    new_information = []
    for meeting in database:
        if meeting['weekday'] != weekday:
            continue
        if meeting['start'] < time_now + datetime.timedelta(minutes = 15) < meeting['end']:
            new_information.append(meeting)
    globals()['information'] = json.dumps(new_information)
    with open('index.html') as f:
        # this is absolutely horrible and we should use nginx
        globals()['index_contents'] = f.read()


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
    return globals()['index_contents']

@route('/data')
def data():
    return globals()['information']

run(host = '0.0.0.0', port = 80, server = 'tornado')
