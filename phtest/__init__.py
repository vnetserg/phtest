import os
from flask import Flask
from flask_session import Session

app = Flask('phtest')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = 'instance/flask_session'
app.secret_key = os.urandom(12)

Session(app)

from . import db

db.init_db()

from . import views
from . import admin


