from flask import flash, redirect, url_for
from flask.views import View
from flask_login import current_user, logout_user
from accessflow.models.activity_log import ActivityLog
from accessflow import db

class AdminLogoutView(View):
    methods = ["GET"]

    def dispatch_request(self):
        if current_user.is_authenticated:
            db.session.add(ActivityLog(
                "logout",
                user = current_user
            ))
            db.session.commit()

            logout_user()
            flash("You have been logged out.", "success")

        return redirect(url_for("admin/login"))