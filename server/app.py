from bottle import route, hook, response, run
import cPickle
import datetime

data = cPickle.load('../data/Spring_2015.bin')
globals()['thingy'] = 'yoyoyo'

@route('/')
def index():
    return globals()['thingy']

run(host = '0.0.0.0', port = 80, server = 'tornado')

