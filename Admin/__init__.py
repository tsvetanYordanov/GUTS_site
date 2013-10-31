from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from guts_website import models

app = Flask(__name__)

# Flask and Flask-SQLAlchemy initialization here

admin = Admin(app)
admin.add_view(ModelView(models.Member, models.db.session))
admin.add_view(ModelView(models.Event, models.db.session))
admin.add_view(ModelView(models.Project, models.db.session))
admin.add_view(ModelView(models.Technology, models.db.session))

app.run()
