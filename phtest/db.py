from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base, User, Question, Answer, Variant, Result

engine = create_engine("sqlite:///instance/db.sqlite")
Base.metadata.create_all(engine)

session = Session(engine)

def get_user_by_login(login):
    if login == "todd":
        return User(1, "Тоддов Василий Петрович", "todd", 1)

def get_user_by_id(uid):
    if uid == 1:
        return User(1, "Тоддов Василий Петрович", "todd", 1)

def get_last_variant(user):
    return None

def save_variant(var):
    pass

def save_user(user):
    pass

def submit_result(result):
    pass

def mark_right_questions(user, question_ids):
    pass
