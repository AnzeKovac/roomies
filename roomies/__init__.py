"""Roomies backend"""

from flask import Flask
from flask_mongoengine import MongoEngine


app = Flask(__name__)


app.config['MONGODB_DB'] = 'heroku_v51tvpq2'
app.config['MONGODB_HOST'] = 'ds139187.mlab.com'
app.config['MONGODB_PORT'] = 39187
app.config['MONGODB_USERNAME'] = 'heroku_v51tvpq2'
app.config['MONGODB_PASSWORD'] = 'i4i37ltt2o995710j0hplnikhc'
app.config['DEBUG'] = True

db = MongoEngine(app)

# import routes after we initialize "app" and "db"
from . import routes
