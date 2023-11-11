from os.path import exists

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from myapp.config import Config
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)
mail = Mail(app)

login = LoginManager(app)

from myapp import models, routes


@login.user_loader
def load_user(id):
    return db.session.get(models.User, int(id))
