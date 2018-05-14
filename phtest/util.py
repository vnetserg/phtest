from datetime import datetime
from . import db

def get_user_from_session(session):
    uid = session.get("user_id")
    if uid is None:
        return None
    user = db.get_user_by_id(uid)
    return user

def make_variant(user):
    return db.Variant(user_id=1, started=datetime.now(), questions=[
        db.Question(section_id=1, text="Как зовут начальника АГЗ?", answers=[
            db.Answer(text="Панченков В.В.", is_correct=True),
            db.Answer(text="Овсянников Р. Е.", is_correct=False),
            db.Answer(text="Агамов Н. А.", is_correct=False),
        ]),
        db.Question(section_id=1, text="Любимое число старшины роты?", answers=[
            db.Answer(text="1", is_correct=False),
            db.Answer(text="2", is_correct=False),
            db.Answer(text="3", is_correct=False),
            db.Answer(text="1.5", is_correct=True)
        ])
    ])
