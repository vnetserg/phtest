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
    if login == app.config["ADMIN_LOGIN"]:
        session["is_admin"] = True
        if "user_id" in session:
            del session["user_id"]
        return redirect(url_for('admin.index'))
    user = db.get_user_by_login(login)
    if user is None:
        return login_failed
    if "is_admin" in session:
        del session["is_admin"]
    session["user_id"] = user.id
    return redirect(url_for('testlist'))


@app.route('/logout', methods=['GET'])
def logout():
    if "user_id" in session:
        del session["user_id"]
    if "is_admin" in session:
        del session["is_admin"]
    return redirect(url_for('index'))


@app.route('/testlist', methods=['GET', 'POST'])
def testlist():
    user = util.get_user_from_session(session)
    if user is None:
        return redirect(url_for('index'))
        
    var = db.get_last_variant(user)
    continue_test = not util.variant_expired(var)
    no_questions = not continue_test and db.no_questions(user)
    
    return render_template('testlist.html', user=user,
            continue_test=continue_test, no_questions=no_questions)


@app.route('/test', methods=['GET'])
def test():
    user = util.get_user_from_session(session)
    if user is None:
        return redirect(url_for('index'))
    if user.attempts <= 0:
        return redirect(url_for('testlist'))

    var = db.get_last_variant(user)
    if util.variant_expired(var):
        var = util.make_variant(user)
        if not var.questions:
            return redirect(url_for('testlist'))
        db.save_variant(var)
        user.attempts -= 1
        db.save_user(user)

    return render_template('test.html', questions=var.questions)


@app.route('/result', methods=['POST'])
def result():
    user = util.get_user_from_session(session)
    if user is None:
        return redirect(url_for('index'))

    var = db.get_last_variant(user)
    if util.variant_expired(var):
        return redirect(url_for('testlist'))
    
    is_chosen = {}
    ans_ids = set(request.form.getlist("answer", int))
    right_qst_ids = set()
    result = {"n_correct": 0, "n_wrong": 0, "n_total": 0}
	
    for qst in var.questions:
        for ans in qst.answers:
            is_chosen[ans] = ans.id in ans_ids
        if qst.answer_correct(ans_ids):
            result["n_correct"] += 1
            right_qst_ids.add(qst.id)
        else:
            result["n_wrong"] += 1
        result["n_total"] += 1

    db.mark_right_questions(user, right_qst_ids)
    db.submit_result(var.make_result(result["n_correct"]))

    return render_template('result.html', questions=var.questions,
                           is_chosen=is_chosen, result=result,
                           success_ratio=app.config["GRADE_RATIOS"][0],
                           de=[0.5] * 6)
