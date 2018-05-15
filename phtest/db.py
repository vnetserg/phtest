from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from .models import Base, User, Question, Answer, Variant, Result

engine = create_engine("sqlite:///instance/db.sqlite")
Base.metadata.create_all(engine)

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

def get_user_by_login(login):
    return session.query(User).filter(User.login == login).scalar()

def get_user_by_id(uid):
    return session.query(User).filter(User.id == uid).scalar()

def get_last_variant(user):
    return session.query(Variant).filter(Variant.user_id == user.id) \
            .order_by(Variant.started.desc()).first()

def save_variant(var):
    session.add(var)
    session.commit()

def save_user(user):
    session.add(user)
    session.commit()

def submit_result(result):
    session.add(result)
    session.commit()

def mark_right_questions(user, question_ids):
    questions = session.query(Question).filter(Question.id.in_(question_ids)).all()
    user.right_questions.extend(questions)
    session.add(user)
    session.commit()
