from flask import render_template, session, request, redirect, url_for

from phtest import app
from . import db

@app.route('/', methods=['GET'])
def index():
    noauth = bool(request.args.get("noauth"))
    return render_template('index.html', noauth=noauth)

@app.route('/login', methods=['POST'])
def login():
    login_failed = redirect(url_for('index', noauth=1))
    login = request.form.get("login")
    if login is None:
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
    uid = session.get("user_id")
    need_login = redirect(url_for('index'))
    if uid is None:
        return need_login
    else:
        user = db.get_user_by_id(uid)
    if user is None:
        return need_login
    return render_template('testlist.html', user=user)

@app.route('/test', methods=['GET'])
def test():
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
    return render_template('test.html', questions=questions)
