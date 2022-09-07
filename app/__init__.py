from flask import Flask
from config import Config

#import blueprint
from .auth.routes import auth

app= Flask(__name__)

# register blueprint
app.register_blueprint(auth)

app.config.from_object(Config)

# initialize our database to work with our app
from .models import db
from flask_migrate import Migrate

db.init_app(app)
migrate = Migrate(app, db)

from . import routes
from . import models