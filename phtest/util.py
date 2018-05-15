from datetime import datetime
from . import db

def get_user_from_session(session):
    uid = session.get("user_id")
    if uid is None:
        return None
    user = db.get_user_by_id(uid)
    return user

def make_variant(user):
    questions = db.session.query(Questions).all()
    return db.Variant(user_id=1, started=datetime.now(), questions=questions)
