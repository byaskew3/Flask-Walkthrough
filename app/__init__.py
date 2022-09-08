import imp
from flask import Flask
from config import Config
from flask_login import LoginManager

#import blueprint
from .auth.routes import auth
from .ig.routes import ig
from .models import User


app= Flask(__name__)
login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)
# register blueprint
app.register_blueprint(auth)
app.register_blueprint(ig)

app.config.from_object(Config)

# initialize our database to work with our app
from .models import db
from flask_migrate import Migrate

db.init_app(app)
migrate = Migrate(app, db)
login.init_app(app)

from . import routes
from . import models