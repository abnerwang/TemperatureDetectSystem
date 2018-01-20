from flask import render_template

from . import main


@main.route('/index/<message>')
def index(message):
    render_template('main/index.html', message=message)
