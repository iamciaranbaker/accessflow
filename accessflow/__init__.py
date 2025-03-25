from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from accessflow.handlers.gitlab import GitLabHandler
from accessflow.config import Config
from accessflow.logger import get_logger
from accessflow.filters import format_time

logger = get_logger()

app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "danger"

gitlab_handler = GitLabHandler()

from accessflow.models.permission import Permission
from accessflow.models.permission_group import PermissionGroup
from accessflow.models.user import User
from accessflow.models.user_permission import UserPermission
from accessflow.models.job import Job
from accessflow.models.job_run import JobRun
from accessflow.models.job_log import JobLog
from accessflow.models.request import Request
from accessflow.models.service import Service
from accessflow.models.pid import PID
from accessflow.models.team import Team

migrate = Migrate(app, db, compare_type = True)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.filters["format_time"] = format_time

from accessflow.views.index import IndexView
from accessflow.views.dashboard import DashboardView
from accessflow.views.requests.list import RequestListView
from accessflow.views.admin.users.list import UserListView
from accessflow.views.admin.users.create import UserCreateView
from accessflow.views.admin.users.delete import UserDeleteView
from accessflow.views.admin.services.list import ServiceListView
from accessflow.views.admin.services.create import ServiceCreateView
from accessflow.views.admin.services.delete import ServiceDeleteView
from accessflow.views.admin.jobs.list import JobListView
from accessflow.views.admin.jobs.logs import JobLogsView
from accessflow.views.admin.jobs.run import JobRunView
from accessflow.views.auth.login import LoginView
from accessflow.views.auth.login_two_factor import LoginTwoFactorView
from accessflow.views.auth.logout import LogoutView

# General Routes
app.add_url_rule("/", view_func = IndexView.as_view("index"))
app.add_url_rule("/dashboard", view_func = DashboardView.as_view("dashboard"))
app.add_url_rule("/requests", view_func = RequestListView.as_view("requests"))
# Admin Routes
app.add_url_rule("/admin/users", view_func = UserListView.as_view("admin/users"))
app.add_url_rule("/admin/users/create", view_func = UserCreateView.as_view("admin/users/create"))
app.add_url_rule("/admin/users/<int:user_id>/delete", view_func = UserDeleteView.as_view("admin/users/delete"))
app.add_url_rule("/admin/services", view_func = ServiceListView.as_view("admin/services"))
app.add_url_rule("/admin/services/create", view_func = ServiceCreateView.as_view("admin/services/create"))
app.add_url_rule("/admin/services/<int:service_id>/delete", view_func = ServiceDeleteView.as_view("admin/services/delete"))
app.add_url_rule("/admin/jobs", view_func = JobListView.as_view("admin/jobs"))
app.add_url_rule("/admin/jobs/logs", view_func = JobLogsView.as_view("admin/jobs/logs"))
app.add_url_rule("/admin/jobs/run", view_func = JobRunView.as_view("admin/jobs/run"))
# Auth Routes
app.add_url_rule("/login", view_func = LoginView.as_view("login"))
app.add_url_rule("/login/two-factor", view_func = LoginTwoFactorView.as_view("login/two-factor"))
app.add_url_rule("/logout", view_func = LogoutView.as_view("logout"))

@app.cli.command("seed-db")
def seed_database():
    PermissionGroup.seed_all()
    Permission.seed_all()
    User.seed_default()
    Job.seed_all()

# For use during development ONLY
@app.cli.command("recreate-db")
def recreate_database():
    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()

@app.cli.command("run-jobs")
def run_jobs():
    Job.run_all()

"""
Temporarily method to create a dummy request whilst testing request system.
"""
@app.cli.command("create-request")
def create_request():
    request = Request(
        pid = 8904064,
        service_id = 1,
        justification = "I am part of the CIS Live Support team."
    )
    db.session.add(request)
    db.session.commit()