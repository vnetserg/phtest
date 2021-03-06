from datetime import datetime
import random

from . import app
from . import db

def get_user_from_session(session):
    uid = session.get("user_id")
    if uid is None:
        return None
    user = db.get_user_by_id(uid)
    return user

def variant_expired(var):
    return var is None or db.variant_finished(var) \
        or (datetime.now() - var.started).seconds > 90 * 60

def make_variant(user):
    sections_count = {i: count for i, count in
                      enumerate(app.config["SECTIONS_COUNT"], start=1)}
    questions = set(db.get_unanswered_questions(user))

    sec_questions = {}
    for qst in questions:
        if qst.section_id in sec_questions:
            sec_questions[qst.section_id].append(qst)
        else:
            sec_questions[qst.section_id] = [qst]

    chosen = []
    for sec, s_qst in sec_questions.items():
        if sec not in sections_count:
            continue
        cnt = sections_count[sec]
        if len(s_qst) <= cnt:
            subset = s_qst
        else:
            subset = random.sample(s_qst, cnt)
        chosen.extend(subset)
        questions -= set(subset)

    need = sum(sections_count.values()) - len(chosen)
    if need > 0:
        if len(questions) > need:
            chosen.extend(random.sample(questions, need))
        else:
            chosen.extend(questions)

    random.shuffle(chosen)

    return db.Variant(user_id=user.id, started=datetime.now(),
                      questions=chosen)
