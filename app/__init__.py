from flask import Flask
from config import Config
from jinja2 import Environment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes

from flask_cors import CORS
from flask_session import Session

jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config['JSON_AS_ASCII'] = False

Session(app)
CORS(app)