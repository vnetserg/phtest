SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = "instance/flask_session"
SECRET_KEY = b"CHANGE_ME"
ADMIN_LOGIN = "admin"
SECTIONS_COUNT = [4, 4, 4, 4, 4, 4]
SQLA_DATABASE_URI = "sqlite:///instance/db.sqlite"
DEBUG = True


import os

try:
    exec(open(os.path.join(os.path.dirname(__file__), "instance",
                           "config.py")).read(), globals())
except FileNotFoundError:
    pass
