from flask import render_template, flash, redirect, request, Response
from flask.wrappers import Request
from app import app
import json
from wtforms import TextField, SubmitField, Form
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
class SearchForm(FlaskForm):
    autocomp = TextField('Station 1', id = 'city_autocomplete', validators = [DataRequired()])
    autocomp1 = TextField('Station 2', id = 'ity_autocomplete', validators = [DataRequired()])
    submit = SubmitField()

cities = ['']
f = open("E:/databasa.txt", "r", encoding='utf-8')
i = 0
k = 0
name = "" 
buf = ""
N = 0   
x = 1.1
y = 1.1
points = []
names = []
for line in f:
    N = N + 1
    i = 0
    while(line[i] != '3' or line[i+1] != '7' or line[i+2] != '.'):
        name = name + line[i]
        i = i + 1
    name = name[:len(name)-1]
    names.append(name)
    name = ''  
cities = names
@app.route('/_autocomplete', methods=['GET'])
def autocomplete(): 
    return Response(json.dumps(cities), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
    bus1 = ''
    bus2 = ''
    form = SearchForm(request.form)
    if form.validate_on_submit():
        bus1 = form.autocomp.data
        bus2 = form.autocomp1.data
        print(bus1)
        print(bus2)
        return render_template("search.html", form=form)
    return render_template("search.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")
