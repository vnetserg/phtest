import math
import datetime
import urllib.parse

from flask import request, session, url_for, redirect
from flask_admin.model.template import EndpointLinkRowAction
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

class AuthRequiredBaseView(BaseView):
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
    column_filters = ["name", "group", "login", "attempts"]
    column_list = column_filters + ["n_answered"]
    column_labels = {
        "name": "ФИО",
        "group": "Группа",
        "login": "Логин",
        "attempts": "Осталось попыток",
        "n_answered": "Отвечено вопросов"
    }
    column_formatters = {
        "n_answered": lambda v, c, m, p: len(m.right_questions)
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

    @action('reset', 'Очистить ответы')
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
    column_default_sort = "text"
    column_filters = ["text", "section_id"]

class ResultModelView(AuthRequiredView):
    column_extra_row_actions = [
        EndpointLinkRowAction('glyphicon icon-eye-open', 'studentresults.index')
    ]
    column_list = ["user", "grade", "n_correct", "n_total", "datetime"]
    column_labels = {
        "n_correct": "Правильных ответов",
        "n_total": "Всего вопросов",
        "grade": "Оценка",
        "datetime": "Время окончания",
        "de_0": "Освоение ДЕ №1",
        "de_1": "Освоение ДЕ №2",
        "de_2": "Освоение ДЕ №3",
        "de_3": "Освоение ДЕ №4",
        "de_4": "Освоение ДЕ №5",
        "de_5": "Освоение ДЕ №6",
        "user": "Пользователь",
        "user.name": "Пользователь / ФИО",
        "user.group": "Пользователь / Группа",
        "user.login": "Пользователь / Логин",
        "user.attempts": "Пользователь / Число попыток",
    }
    column_formatters = {
        "datetime": lambda v, c, m, p: m.datetime.strftime("%H:%M:%S %d.%m.%Y"),
        "user": lambda v, c, m, p: f"{m.user.name} ({m.user.group})",
        "grade": lambda v, c, m, p: "отл." if m.n_correct / m.n_total >= app.config["GRADE_RATIOS"][2] else "хор." if m.n_correct / m.n_total >= app.config["GRADE_RATIOS"][1] else "удов." if m.n_correct / m.n_total >= app.config["GRADE_RATIOS"][0] else "неуд."
    }
    column_filters = ["user.name", "user.login", "user.group", "user.attempts",
                      "n_correct", "n_total", "datetime"]
    column_exclude_list = ["variant"]
    form_excluded_columns = ["variant"]

    column_sortable_list = [("user", "user.name"), "n_correct",
                            "n_total", "datetime"]
    column_default_sort = ("datetime", True)

    def is_editable(self, name):
        return False

class StudentResultView(AuthRequiredBaseView):
    @expose("/", methods=["GET"])
    def index(self):
        rid = request.args.get("id")
        if rid is None:
            return redirect("/admin/result")
        result = db.get_result_by_id(rid)
        if result is None:
            return redirect("/admin/result")
        ratio = result.n_correct / result.n_total
        grade_ind = [i for i in range(4) if ratio < (app.config["GRADE_RATIOS"] + [2])[i]][0]
        return self.render("admin/studentresults.html", user=result.user,
                           result=result, date=result.datetime,
                           grade_ind=grade_ind)

class ReportView(AuthRequiredBaseView):
    @expose("/")
    def index(self):
        groups = sorted(db.get_all_groups())
        return self.render("admin/groups.html", group_url=url_for(".report"),
                           groups=groups, quote=urllib.parse.quote)
    
    @expose("/group", methods=["GET"])
    def report(self):
        group = request.args.get("group")
        if group is None:
            return redirect(url_for(".index"))
        pad = lambda x: "_" * math.ceil((20 - len(str(x))) / 2) + str(x) \
                            + "_" * math.floor((20 - len(str(x))) / 2)
        group_grade_count = db.get_group_grade_count(group)
        group_params = {
            "group": group,
            "students_count": db.count_group_students(group),
            "testing_students_count": db.count_participated_group_students(group),
            "A_degree": group_grade_count[3],
            "B_degree": group_grade_count[2],
            "C_degree": group_grade_count[1],
            "D_degree": group_grade_count[0],
        }
        return self.render("admin/groupreport.html",
                           group={k: pad(v) for k, v in group_params.items()},
                           date=datetime.date.today())

class LogoutView(BaseView):
    @expose("/")
    def index(self):
        return redirect(url_for("logout"))

admin = Admin(app, name="Тесторивание ФП", index_view=AdminAuthIndexView())

admin.add_view(UserModelView(db.User, db.session, name="Пользователи"))
admin.add_view(QuestionModelView(db.Question, db.session, name="Вопросы"))
admin.add_view(ResultModelView(db.Result, db.session, name="Результаты"))
admin.add_view(ReportView(name="Отчёты", endpoint="report"))
admin.add_view(LogoutView(name="Выйти", endpoint="logout"))
admin.add_view(StudentResultView(name="", endpoint="studentresults"))


babel = Babel(app)

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'ru')
