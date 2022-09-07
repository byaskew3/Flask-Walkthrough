from app import app
from flask import render_template

@app.route('/')
def home():
    students = ['Robert', 'Julian', 'Ian', 'Logan', 'Mason', 'Christian']
    return render_template('home.html', names=students)

@app.route('/movies')
def movies():
    return render_template('movies.html')