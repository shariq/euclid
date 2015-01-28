import cPickle
import datetime
import threading
import time
import json
from bottle import route, hook, response, run

database = cPickle.load('../data/Spring_2015.bin')

globals()['information'] = ''

def updateInformation():
    weekday = datetime.datetime.now().weekday()
    time = datetime.datetime.now().time()
    new_information = []
    for course in database.keys():
        description = database[course]['description']
        title = database[course]['title']
        for meeting in meetings:
            if meeting['weekday'] != weekday:
                continue
            if meeting['start'] < time < meeting['end']:
                new_information.append((title, description, meeting))
    globals()['information'] = json.dumps(new_information)

def updateThread():
    while True:
        updateInformation()
        time.sleep(60)

updateInformation()
looper = threading.Thread(updateThread)
looper.daemon = True
looper.start()

@route('/')
def index():
    return 'yoyoyo'

@route('/data')
def data():
    return globals()['information']

run(host = '0.0.0.0', port = 80, server = 'tornado')
