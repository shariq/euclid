from bottle import route, hook, response, run
import random

globals()['thingy'] = 'yoyoyo'

@route('/')
def index():
    return globals()['thingy']

run(host = '0.0.0.0', port = 80, server = 'tornado')

