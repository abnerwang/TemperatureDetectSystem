from flask import render_template

from . import main


@main.route('/index/<message>')
def index(message):
    return render_template('main/index.html', message=message)
