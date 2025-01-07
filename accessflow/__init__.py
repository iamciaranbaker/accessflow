from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from accessflow.config import Config

app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "danger"

from accessflow.models.user import User
from accessflow.models.permission import Permission
from accessflow.models.user_permission import UserPermission

migrate = Migrate(app, db, compare_type=True)

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id = id).first()

from accessflow.scripts.seed import seed_database

from accessflow.views.dashboard import DashboardView
from accessflow.views.requests import RequestsView
from accessflow.views.authentication.login import LoginView
from accessflow.views.authentication.logout import LogoutView
from accessflow.views.directory.users import DirectoryUsersView
from accessflow.views.directory.groups import DirectoryGroupsView
from accessflow.views.directory.services import DirectoryServicesView
from accessflow.views.administration.users import AdministrationUsersView
from accessflow.views.administration.create_user import AdministrationCreateUserView
from accessflow.views.administration.logs import AdministrationLogsView

app.add_url_rule("/dashboard", view_func = DashboardView.as_view("dashboard"))
app.add_url_rule("/requests", view_func = RequestsView.as_view("requests"))
app.add_url_rule("/login", view_func = LoginView.as_view("login"))
app.add_url_rule("/logout", view_func = LogoutView.as_view("logout"))
app.add_url_rule("/directory/users", view_func = DirectoryUsersView.as_view("directory/users"))
app.add_url_rule("/directory/groups", view_func = DirectoryGroupsView.as_view("directory/groups"))
app.add_url_rule("/directory/services", view_func = DirectoryServicesView.as_view("directory/services"))
app.add_url_rule("/administration/users", view_func = AdministrationUsersView.as_view("administration/users"))
app.add_url_rule("/administration/users/create", view_func = AdministrationCreateUserView.as_view("administration/users/create"))
app.add_url_rule("/administration/logs", view_func = AdministrationLogsView.as_view("administration/logs"))