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

from accessflow.models.permission_type import PermissionType
from accessflow.models.permission import Permission
from accessflow.models.user import User, get_all_users
from accessflow.models.user_permission import UserPermission

migrate = Migrate(app, db, compare_type=True)

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id = id).first()

from accessflow.scripts.seed import seed_database
from accessflow.utils import get_all_permissions
from accessflow.utils import get_permission_type_by_id
from accessflow.utils import get_permission_type_by_name

app.jinja_env.globals["get_all_permissions"] = get_all_permissions
app.jinja_env.globals["get_permission_type_by_id"] = get_permission_type_by_id
app.jinja_env.globals["get_permission_type_by_name"] = get_permission_type_by_name
app.jinja_env.globals["get_all_users"] = get_all_users

from accessflow.views.index import IndexView
from accessflow.views.dashboard import DashboardView
from accessflow.views.requests.list import RequestListView
from accessflow.views.admin.users.list import UserListView
from accessflow.views.admin.users.create import UserCreateView
from accessflow.views.admin.logs.list import LogListView
from accessflow.views.auth.login import LoginView
from accessflow.views.auth.logout import LogoutView

# General Routes
app.add_url_rule("/", view_func = IndexView.as_view("index"))
app.add_url_rule("/dashboard", view_func = DashboardView.as_view("dashboard"))
app.add_url_rule("/requests", view_func = RequestListView.as_view("requests"))
# Admin Routes
app.add_url_rule("/admin/users", view_func = UserListView.as_view("admin/users"))
app.add_url_rule("/admin/users/create", view_func = UserCreateView.as_view("admin/users/create"))
app.add_url_rule("/admin/logs", view_func = LogListView.as_view("admin/logs"))
# Auth Routes
app.add_url_rule("/login", view_func = LoginView.as_view("login"))
app.add_url_rule("/logout", view_func = LogoutView.as_view("logout"))