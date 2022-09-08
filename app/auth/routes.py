from flask import Blueprint, render_template, request, redirect, url_for
from .forms import LoginForm, UserCreationForm

#import login functionality
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

#import models
from app.models import User

auth = Blueprint('auth', __name__, template_folder='authtemplates')

from app.models import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            # Query user based off of username
            user = User.query.filter_by(username=username).first()
            print(user.id, user.username, user.password)
            if user:
                # compare passwords
                if check_password_hash(user.password, password):
                    login_user(user)
                else:
                    print('Incorrect Password')
            else:
                #if user doesnt exist
                pass
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
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