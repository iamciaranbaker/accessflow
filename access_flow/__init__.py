from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from access_flow.config import Config

app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "danger"

from access_flow.models.user import User
import access_flow.views

migrate = Migrate(app, db, compare_type = True)

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id = id).first()