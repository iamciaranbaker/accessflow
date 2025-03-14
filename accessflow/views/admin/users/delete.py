from flask import request, flash, redirect, url_for, abort
from flask.views import View
from flask_login import login_required, current_user
from accessflow.decorators import permission_required
from accessflow.models.user_permission import UserPermission
from accessflow.models.user import User
from accessflow import db

class UserDeleteView(View):
    methods = ["GET"]
    decorators = [login_required, permission_required("delete_users")]

    def dispatch_request(self, user_id):
        # The user shouldn't be able to delete themselves.
        # The UI should prevent this from happening, but return a 500 error just in case
        if current_user.id == user_id:
            abort(500)

        # Delete all records across all tables associated with the specified user
        user_permissions = UserPermission.query.filter(UserPermission.user_id == user_id).delete()
        user = User.query.filter(User.id == user_id).delete()

        # Check the user ID is actually valid
        if not user_permissions or not user:
            abort(404)

        #db.session.commit()

        flash("User has been deleted successfully.", "success")

        return redirect(url_for("admin/users"))