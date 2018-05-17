import os

from sqlalchemy import create_engine, func, cast, Float
from sqlalchemy.interfaces import PoolListener
from sqlalchemy.orm import sessionmaker, scoped_session, aliased

from . import app
from .models import Base, User, Question, Answer, Variant, Result


if os.path.isabs(app.config["SQLITE_PATH"]):
    sqla_uri = os.path.join("sqlite:////", app.config["SQLITE_PATH"])
else:
    sqla_uri = "sqlite:///" + os.path.join(os.path.dirname(os.path.dirname(__file__)), app.config["SQLITE_PATH"])


class ForeignKeysListener(PoolListener):
    def connect(self, dbapi_con, con_record):
        db_cursor = dbapi_con.execute('pragma foreign_keys=ON')

engine = create_engine(sqla_uri, listeners=[ForeignKeysListener()])

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

def get_all_groups():
    return [x[0] for x in session.query(User.group).distinct(User.group).all()]

def no_questions(user):
    qst_ids = [qst.id for qst in user.right_questions]
    return session.query(Question).filter(~Question.id.in_(qst_ids)).limit(1).first() is None

def variant_finished(var):
    return session.query(Result).filter(Result.variant_id == var.id).limit(1).count() == 1

def get_group_grade_count(group):
    res = session.query(func.max(cast(Result.n_correct, Float) / Result.n_total), User.id).group_by(Result.user_id).join(User).filter(User.group == group).all()
    grades = {uid: grade for grade, uid in res}

    variants = session.query(Variant).join(User).filter(User.group == group).all()
    for var in variants:
        if var.user_id not in grades:
            grades[var.user_id] = 0

    ths = app.config["GRADE_RATIOS"]
    return [sum(1 for g in grades.values() if lo <= g < hi) for lo, hi in zip(
                [-1] + ths, ths + [2])]

def count_group_students(group):
    return session.query(func.count(User.id.distinct())).filter(User.group == group).one()[0]

def count_participated_group_students(group):
    var_uids = {x[0] for x in session.query(Variant.user_id).join(User).filter(User.group == group).all()}
    res_uids = {x[0] for x in session.query(Result.user_id).join(User).filter(User.group == group).all()}
    return len(var_uids | res_uids)
