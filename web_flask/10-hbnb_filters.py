#!/usr/bin/python3
''' flask web application for task 3
    0x04. AirBnB clone - Web framework
'''

from flask import Flask, escape, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


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


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pythontext(text='is cool'):
    '''returns a test message'''
    return 'Python {}'.format(escape(text).replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def numberRoute(n):
    '''returns a test message'''
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def templateRoute(n):
    '''returns a test template'''
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def template_odd_even_Route(n):
    '''returns a test template'''
    return render_template('6-number_odd_or_even.html', number=n)


@app.route('/states_list', strict_slashes=False)
def states_list():
    '''lists available states'''
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    '''lists available states with there cities'''
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id=0):
    '''list states by there id and there cities or just states'''
    state_id = 'State.' + str(id)
    states = storage.all(State)
    return render_template('9-states.html', state_id=state_id, states=states)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    '''show states and cities in my airbnb page filters'''
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities)


@app.teardown_appcontext
def teardown_app(exception):
    '''teardown the app , closes current sqlalchemy session'''
    storage.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
