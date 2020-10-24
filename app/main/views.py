from . import main
from flask import render_template
from flask import request

from .forms import PitchForm

@main.route('/')
def index():

    return render_template("index.html")

@main.route('/post')
def pitch():
    title= request.args.get('title')
    content= request.args.get('content')
    category= request.args.get('id')

    return render_template("pitch.html")
