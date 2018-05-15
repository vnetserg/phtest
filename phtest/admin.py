from flask import request, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel

from phtest import app, db


admin = Admin(app)

class UserModelView(ModelView):
    column_default_sort = "name"
    column_labels = {
        "name": "ФИО",
        "login": "Логин",
        "attempts": "Число попыток"
    }
    form_excluded_columns = ("right_questions",)

class QuestionModelView(ModelView):
    inline_models = [(db.Answer, {"column_labels": {
        "text": "Текст",
        "is_correct": "Верный"
    }})]
    column_labels = {
        "text": "Текст",
        "section_id": "Номер секции",
        "answers": "Вариант Ответа"
    }
    column_default_sort = ("section_id", "text")

admin.add_view(UserModelView(db.User, db.session, name="Пользователь"))
admin.add_view(QuestionModelView(db.Question, db.session, name="Вопрос"))


babel = Babel(app)

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'ru')
