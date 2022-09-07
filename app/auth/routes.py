from flask import Blueprint, render_template, request, redirect, url_for
from .forms import UserCreationForm

#import models
from app.models import User

auth = Blueprint('auth', __name__, template_folder='authtemplates')

from app.models import db

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserCreationForm()
    if request.method == 'POST':
        print('POST request made')
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            print(username, email, password)

            # add user to database
            user = User(username, email, password)

            # add instance to database
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print('validation failed')
    else:
        print('GET request made')
    return render_template('signup.html', form=form)