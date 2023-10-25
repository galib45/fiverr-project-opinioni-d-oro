import flask
from myapp.database import Database

db = Database('database.db')
app = flask.Flask(__name__)

from myapp import routes
