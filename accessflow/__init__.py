from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException
from accessflow.handlers.gitlab import GitLabHandler
from accessflow.config import Config
from accessflow.logger import get_logger
from accessflow.filters import format_time, format_date, format_datetime
import traceback

logger = get_logger()

app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin/login"
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
app.jinja_env.filters["format_date"] = format_date
app.jinja_env.filters["format_datetime"] = format_datetime

from accessflow.views.index import IndexView
from accessflow.views.requests.create import RequestCreateView
from accessflow.views.admin.dashboard import AdminIndexView
from accessflow.views.admin.requests.list import AdminRequestListView
from accessflow.views.admin.pids.list import AdminPIDListView
from accessflow.views.admin.teams.list import AdminTeamListView
from accessflow.views.admin.services.list import AdminServiceListView
from accessflow.views.admin.services.create import AdminServiceCreateView
from accessflow.views.admin.services.delete import AdminServiceDeleteView
from accessflow.views.admin.users.list import AdminUserListView
from accessflow.views.admin.users.create import AdminUserCreateView
from accessflow.views.admin.users.delete import AdminUserDeleteView
from accessflow.views.admin.jobs.list import AdminJobListView
from accessflow.views.admin.jobs.logs import AdminJobLogsView
from accessflow.views.admin.jobs.run import AdminJobRunView
from accessflow.views.admin.authentication.login import AdminLoginView
from accessflow.views.admin.authentication.login_two_factor import AdminLoginTwoFactorView
from accessflow.views.admin.authentication.logout import AdminLogoutView

app.add_url_rule("/", view_func = IndexView.as_view("index"))
app.add_url_rule("/requests/create", view_func = RequestCreateView.as_view("requests/create"))
"""
Admin Routes
"""
app.add_url_rule("/admin", view_func = AdminIndexView.as_view("admin/index"))
# Requests
app.add_url_rule("/admin/requests", view_func = AdminRequestListView.as_view("admin/requests"))
# PIDs
app.add_url_rule("/admin/pids", view_func = AdminPIDListView.as_view("admin/pids"))
# Teams
app.add_url_rule("/admin/teams", view_func = AdminTeamListView.as_view("admin/teams"))
# Services
app.add_url_rule("/admin/services", view_func = AdminServiceListView.as_view("admin/services"))
app.add_url_rule("/admin/services/create", view_func = AdminServiceCreateView.as_view("admin/services/create"))
app.add_url_rule("/admin/services/delete", view_func = AdminServiceDeleteView.as_view("admin/services/delete"))
# Users
app.add_url_rule("/admin/users", view_func = AdminUserListView.as_view("admin/users"))
app.add_url_rule("/admin/users/create", view_func = AdminUserCreateView.as_view("admin/users/create"))
app.add_url_rule("/admin/users/delete", view_func = AdminUserDeleteView.as_view("admin/users/delete"))
# Jobs
app.add_url_rule("/admin/jobs", view_func = AdminJobListView.as_view("admin/jobs"))
app.add_url_rule("/admin/jobs/logs", view_func = AdminJobLogsView.as_view("admin/jobs/logs"))
app.add_url_rule("/admin/jobs/run", view_func = AdminJobRunView.as_view("admin/jobs/run"))
# Authentication
app.add_url_rule("/admin/login", view_func = AdminLoginView.as_view("admin/login"))
app.add_url_rule("/admin/login/two-factor", view_func = AdminLoginTwoFactorView.as_view("admin/login/two-factor"))
app.add_url_rule("/admin/logout", view_func = AdminLogoutView.as_view("admin/logout"))

@app.errorhandler(Exception)
def handle_exception(exception):
    try:
        code = exception.code
    except:
        code = 500

    if not isinstance(exception, HTTPException):
        traceback.print_tb(exception.__traceback__)

    match code:
        case 401:
            return {"success": False, "error": "You are not authenticated."}, code
        case 403:
            return {"success": False, "error": "You do not have the required permission."}, code
        case 404:
            return {"success": False, "error": f"The route {request.path} does not exist."}, code
        case _:
            return {"success": False, "error": "There was an unexpected server error."}, code

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