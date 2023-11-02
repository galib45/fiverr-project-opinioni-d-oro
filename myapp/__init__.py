from os.path import exists
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate

class Base(DeclarativeBase): pass
db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a380d337493dc430200b3d31ef9a06fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

login = LoginManager(app)

from myapp import routes, models

@login.user_loader
def load_user(id):
    return db.session.get(models.User, int(id))
