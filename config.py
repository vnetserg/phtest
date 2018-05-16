SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = "instance/flask_session"
SECRET_KEY = b"CHANGE_ME"
SQLA_DATABASE_URI = "sqlite:///instance/db.sqlite"
DEBUG = True

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

ADMIN_LOGIN = "admin"
SECTIONS_COUNT = [4, 4, 4, 4, 4, 4]
GRADE_RATIOS = [0.6, 0.7, 0.8]


import os

try:
    exec(open(os.path.join(os.path.dirname(__file__), "instance",
                           "config.py")).read(), globals())
except FileNotFoundError:
    pass
