#!/usr/bin/python3
''' flask web application for task 2
    0x04. AirBnB clone - Web framework
'''

from flask import Flask, escape


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    '''returns a hello message'''
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''returns a hello message'''
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def ctext(text):
    '''returns a test message'''
    return 'C {}'.format(escape(text).replace('_', ' '))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
