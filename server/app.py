#!/usr/bin/env python

import cPickle
import datetime
import threading
import time
import json
import re
from bottle import route, hook, response, run, static_file

database = cPickle.load(open('../data/Spring_2015.bin', 'rb'))

globals()['information'] = ''


def updateInformation():
    weekday = datetime.datetime.now().weekday()
    time = datetime.datetime.now().time()
    new_information = []
    for course in database.keys():
        description = database[course]['description']
        description = re.sub(r'(Formerly:|Restriction:|Prerequisite:|Credit only granted for:|Or permission of) .*?[.] ?', '', description)
        description = description.strip()
        title = database[course]['title']
        for meeting in database[course]['meetings']:
            if meeting['weekday'] != weekday:
                continue
            if meeting['start'] < time < meeting['end']:
                if meeting['location'] == 'TBA':
                    continue
                new_meeting = meeting.copy()
                new_meeting['start'] = new_meeting['start'].strftime('%I:%M %p')
                new_meeting['end'] = new_meeting['end'].strftime('%I:%M %p')
                new_meeting['title'] = title
                new_meeting['code'] = course
                new_meeting['description'] = description
                new_information.append(new_meeting)
    globals()['information'] = json.dumps(new_information)


def updateThread():
    while True:
        updateInformation()
        time.sleep(60)


index_contents = open('index.html').read()
# this is absolutely horrible and we should use nginx

updateInformation()
looper = threading.Thread(target = updateThread)
looper.daemon = True
looper.start()

@route('/')
def index():
    return index_contents

@route('/data')
def data():
    return globals()['information']

run(host = '0.0.0.0', port = 80, server = 'tornado')
