from flask import Flask
from flask_login import LoginManager
from myapp.database import Database

db = Database('database.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a380d337493dc430200b3d31ef9a06fd'
login = LoginManager(app)

@login.user_loader
def load_user(id):
    return db.get_user_by_id(id)

from myapp import routes
