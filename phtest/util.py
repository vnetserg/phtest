from datetime import datetime
from . import db

def get_user_from_session(session):
    uid = session.get("user_id")
    if uid is None:
        return None
    user = db.get_user_by_id(uid)
    return user

def make_variant(user):
    questions = [
        {"id": 1, "text": "Как зовут начальника АГЗ?", "answers": [
            {"id": 101, "text": "Панченков В. В."},
            {"id": 102, "text": "Овсянников Р. Е."},
            {"id": 103, "text": "Агамов Н. А."}
        ]},
        {"id": 2, "text": "Любимое число старшины роты?", "answers": [
            {"id": 104, "text": "1"},
            {"id": 105, "text": "2"},
            {"id": 106, "text": "3"},
            {"id": 107, "text": "1.5"}
        ]},
    ]
    return db.Variant(1, user.id, questions, datetime.now())
