from flask import request, flash, redirect, url_for, abort
from flask.views import View
from flask_login import login_required
from accessflow.models.user_permission import UserPermission
from accessflow.models.user import User
from accessflow import db

class UserDeleteView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self, user_id):
        user_permissions = UserPermission.query.filter(UserPermission.user_id == user_id).delete()
        user = User.query.filter(User.id == user_id).delete()

        if not user_permissions or not user:
            abort(404)

        db.session.commit()

        flash("User has been deleted successfully.", "success")

        return redirect(url_for("admin/users"))