from flask import Flask
from flask_session import Session

app = Flask('phtest', instance_relative_config=True)
app.config.from_object('config')

Session(app)

from . import db

db.init_db()

from . import views
from . import admin


