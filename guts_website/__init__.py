# INIT
# ================================================
# Initialise the application

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure db
app.config.from_object('config')
db = SQLAlchemy(app)

from guts_website import views, models
