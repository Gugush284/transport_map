from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Alexey' }
    return render_template("index.html")
