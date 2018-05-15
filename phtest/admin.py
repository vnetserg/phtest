from flask import request, session, url_for, redirect
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel

from phtest import app, db


admin = Admin(app, name="Тесторивание ФП")

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

class LogoutView(BaseView):
    @expose("/")
    def index(self):
        return redirect(url_for("logout"))

admin.add_view(UserModelView(db.User, db.session, name="Пользователи"))
admin.add_view(QuestionModelView(db.Question, db.session, name="Вопросы"))
admin.add_view(LogoutView(name="Выйти", endpoint="logout"))


babel = Babel(app)

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'ru')
