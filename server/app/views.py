from flask import render_template, flash, redirect, request
from app import app
from app import forms

@app.route('/', methods=["POST", "GET"] )
@app.route('/index', methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
# added URL routes

def login():
    bus1 = ''
    # bus station user typed in form
    bus2 = ''
    # bus station user typed in form
    message = ''
    # message of handling bus1 and bus2
    if request.method == 'GET':
        message = "Enter staion names"
    if request.method == 'POST':
	    bus1 = request.form.get('Station1')
	    bus2 = request.form.get('Station2')
    #form request handling
    if (len(bus1) < 1 or len(bus1) > 100):
        message = "bad data"
    if (len(bus2) < 1 or len(bus2) > 100):
        message = "bad data"
    # simple test of entered data
    return render_template('login.html', message=message)
# function - handler of '/login' request

def index():
    return render_template("index.html")
# function - handler of '/index' request
