from flask import flash, redirect, url_for
from flask.views import View
from flask_login import current_user, logout_user

class LogoutView(View):
    methods = ["GET"]

    def dispatch_request(self):
        if current_user.is_authenticated:
            logout_user()
            flash("You have been logged out.", "success")

        return redirect(url_for("login"))