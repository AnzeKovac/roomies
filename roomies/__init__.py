"""Roomies backend"""
from flask.json import JSONEncoder
from bson.objectid import ObjectId
from flask import Flask
from flask_mongoengine import MongoEngine


class CustomJSONEncoder(JSONEncoder):
    """Custom json decoder. Needs to be initialize in flask config file.
    E.g. app.json_encoder = "class of our custom encoder"
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)


app = Flask(__name__)
app.config['MONGODB_DB'] = 'heroku_v51tvpq2'
app.config['MONGODB_HOST'] = 'ds139187.mlab.com'
app.config['MONGODB_PORT'] = 39187
app.config['MONGODB_USERNAME'] = 'heroku_v51tvpq2'
app.config['MONGODB_PASSWORD'] = 'i4i37ltt2o995710j0hplnikhc'
app.config['DEBUG'] = True
app.json_encoder = CustomJSONEncoder

db = MongoEngine(app)

# import routes after we initialize "app" and "db"
from . import routes
