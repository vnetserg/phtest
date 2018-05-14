from datetime import datetime

from flask import render_template, session, request, redirect, url_for

from phtest import app
from . import db
from . import util


@app.route('/', methods=['GET'])
def index():
    noauth = bool(request.args.get("noauth"))
    return render_template('index.html', noauth=noauth)


@app.route('/login', methods=['POST'])
def login():
    login_failed = redirect(url_for('index', noauth=1))
    login = request.form.get("login")
    if not login:
        return login_failed
    user = db.get_user_by_login(login)
    if user is None:
        return login_failed
    session["user_id"] = user.id
    return redirect(url_for('testlist'))


@app.route('/logout', methods=['GET'])
def logout():
    if "user_id" in session:
        del session["user_id"]
    return redirect(url_for('index'))


@app.route('/testlist', methods=['GET', 'POST'])
def testlist():
    user = util.get_user_from_session(session)
    if user is None:
        return redirect(url_for('index'))
    return render_template('testlist.html', user=user)


@app.route('/test', methods=['GET'])
def test():
    user = util.get_user_from_session(session)
    if user is None:
        return redirect(url_for('index'))
    if user.attempts <= 0:
        return redirect(url_for('testlist'))

    var = db.get_last_variant(user)
    if var is None:
        var = util.make_variant(user)
        db.save_variant(var)

    if (datetime.now() - var.started).seconds > 90 * 60:
        return redirect(url_for('testlist'))

    # user.attempts -= 1
    user = user._replace(attempts = user.attempts - 1)
    db.save_user(user)

    return render_template('test.html', questions=var.questions)


@app.route('/result', methods=['POST'])
def result():
    user = util.get_user_from_session(session)
    if user is None:
        return redirect(url_for('index'))

    var = db.get_last_variant(user)
    if var is None:
        return redirect(url_for('testlist'))

    ans_ids = set(request.form.getlist("answer", int))
    right_ids = set()
    result = {"n_correct": 0, "n_wrong": 0, "n_total": 0}
    for qst in var.questions:
        for ans in qst.answers:
            ans.is_chosen = ans.id in ans_ids
        if qst.answer_correct(ans_ids):
            result["n_correct"] += 1
            right_ids.add(qst.id)
        else:
            result["n_wrong"] += 1
        result["n_total"] += 1

    db.mark_right_questions(user, right_ids)
    db.submit_result(qst.make_result(result["n_correct"]))

    return render_template('test.html', questions=var.questions, result=result)
