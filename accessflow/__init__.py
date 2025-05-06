from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from werkzeug.exceptions import HTTPException
from accessflow.gitlab.gitlab_handler import GitLabHandler
from accessflow.config import Config
from accessflow.filters import format_time, format_date, format_datetime
import traceback
import logging

# Create an additional logging level
logging.SUCCESS = 25 # Between WARNING and INFO
logging.addLevelName(logging.SUCCESS, "SUCCESS")

db = SQLAlchemy()
migrate = Migrate(compare_type = True)
cache = Cache()
login_manager = LoginManager()
gitlab_handler = GitLabHandler()
logger = logging.getLogger()

def create_app():
    app = Flask(__name__, template_folder = "templates", static_folder = "static")
    app.config.from_object(Config)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.filters["format_time"] = format_time
    app.jinja_env.filters["format_date"] = format_date
    app.jinja_env.filters["format_datetime"] = format_datetime

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "admin/login"
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_message_category = "danger"

    app.cache = cache

    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    from accessflow.routes import register_routes
    register_routes(app)

    from accessflow.cli import register_cli
    register_cli(app)

    @app.errorhandler(Exception)
    def handle_exception(exception):
        code = getattr(exception, "code", 500)

        if not isinstance(exception, HTTPException):
            traceback.print_tb(exception.__traceback__)

        if request.path.lower().startswith("/api"):
            return {
                401: {"success": False, "error": "You are not authenticated."},
                403: {"success": False, "error": "You do not have the required permission."},
                404: {"success": False, "error": f"The route {request.path} does not exist."}
            }.get(code, {"success": False, "error": "Unexpected server error."}), code

        return render_template("pages/error.html", code = code), code
    
    return app