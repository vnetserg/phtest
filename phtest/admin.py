from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app)

class QuestionModelView(ModelView):
    inline_models = (db.Answer,)

admin.add_view(ModelView(db.User, db.session))
admin.add_view(QuestionModelView(db.Question, db.session))
