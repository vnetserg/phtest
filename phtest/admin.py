from flask_admin.form import rules

from flask import request, session, url_for, redirect
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel

from phtest import app, db


class AuthRequiredView(ModelView):
    def is_accessible(self):
        return session.get("is_admin") is True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

class AdminAuthIndexView(AdminIndexView):
    def is_accessible(self):
        return session.get("is_admin") is True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

class UserModelView(AuthRequiredView):
    column_default_sort = "name"
    column_labels = {
        "name": "ФИО",
        "group": "Группа",
        "login": "Логин",
        "attempts": "Число попыток"
    }
    form_excluded_columns = ("right_questions",)

    @action('increment', '+1 попытка')
    def action_increment(self, ids):
        users = db.get_all_users_by_id(ids)
        for usr in users:
            usr.attempts += 1
        db.save_user(users)

    @action('zero', 'Сбросить попытки')
    def action_zero(self, ids):
        users = db.get_all_users_by_id(ids)
        for usr in users:
            usr.attempts = 0
        db.save_user(users)

    @action('reset', 'Очистить историю')
    def action_reset(self, ids):
        users = db.get_all_users_by_id(ids)
        for usr in users:
            usr.right_questions = []
        db.save_user(users)

class QuestionModelView(AuthRequiredView):
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

class ResultModelView(AuthRequiredView):
    column_labels = {
        "n_correct": "Правильных ответов",
        "n_total": "Всего вопросов",
        "datetime": "Время окончания",
        "variant": "Пользователь"
    }
    column_formatters = {
        "datetime": lambda v, c, m, p: m.datetime.strftime("%H:%M:%S %d.%m.%Y"),
        "variant": lambda v, c, m, p: f"{m.variant.user.name} ({m.variant.user.group})"
    }
    column_sortable_list = list(column_labels.keys())

    column_default_sort = ("datetime", True)
    action_disallowed_list = ["delete"]

    def is_editable(self, name):
        return False

class LogoutView(BaseView):
    @expose("/")
    def index(self):
        return redirect(url_for("logout"))

admin = Admin(app, name="Тесторивание ФП", index_view=AdminAuthIndexView())

admin.add_view(UserModelView(db.User, db.session, name="Пользователи"))
admin.add_view(QuestionModelView(db.Question, db.session, name="Вопросы"))
admin.add_view(ResultModelView(db.Result, db.session, name="Результаты"))
admin.add_view(LogoutView(name="Выйти", endpoint="logout"))


babel = Babel(app)

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'ru')
