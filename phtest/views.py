from flask import render_template

from phtest import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', noauth=False)

@app.route('/testlist', methods=['GET', 'POST'])
def testlist():
    return render_template('testlist.html', username="Петров Василий", attempts=1)

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
