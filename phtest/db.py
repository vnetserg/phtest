import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from . import app
from .models import Base, User, Question, Answer, Variant, Result

if os.path.isabs(app.config["SQLITE_PATH"]):
    sqla_uri = os.path.join("sqlite:////", app.config["SQLITE_PATH"])
else:
    sqla_uri = "sqlite:///" + os.path.join(os.path.dirname(os.path.dirname(__file__)), app.config["SQLITE_PATH"])

engine = create_engine(sqla_uri)

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

def init_db():
    Base.metadata.create_all(engine)
    session.commit()

def get_user_by_login(login):
    return session.query(User).filter(User.login == login).scalar()

def get_user_by_id(uid):
    return session.query(User).filter(User.id == uid).scalar()

def get_all_users_by_id(uids):
    return session.query(User).filter(User.id.in_(uids)).all()

def get_last_variant(user):
    return session.query(Variant).filter(Variant.user_id == user.id) \
            .order_by(Variant.started.desc()).first()

def get_all_questions():
    return session.query(Question).all()

def save_variant(var):
    session.add(var)
    session.commit()

def save_user(users):
    if not isinstance(users, list):
        users = [users]
    session.add_all(users)
    session.commit()

def save_question(questions):
    if not isinstance(questions, list):
        questions = [questions]
    session.add_all(questions)
    session.commit()

def submit_result(result):
    session.add(result)
    session.commit()

def mark_right_questions(user, question_ids):
    questions = session.query(Question).filter(Question.id.in_(question_ids)).all()
    user.right_questions.extend(questions)
    session.add(user)
    session.commit()

def get_unanswered_questions(user):
    qst_ids = [qst.id for qst in user.right_questions]
    return session.query(Question).filter(~Question.id.in_(qst_ids)).all()

def no_questions(user):
    qst_ids = [qst.id for qst in user.right_questions]
    return session.query(Question).filter(~Question.id.in_(qst_ids)).limit(1).first() is None


def variant_finished(var):
    return session.query(Result).filter(Result.variant_id == var.id).limit(1).count() == 1
