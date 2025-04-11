from flask import request, flash, redirect, url_for, abort
from flask.views import View
from flask_login import login_required, current_user
from accessflow.decorators import permission_required
from accessflow.models.user_permission import UserPermission
from accessflow.models.user import User
from accessflow import db

class AdminUserDeleteView(View):
    methods = ["GET"]
    decorators = [permission_required("delete_users"), login_required]

    def dispatch_request(self):
        # Fetch the id query parameter
        try:
            user_id = int(request.args.get("id"))
        except:
            abort(404)

        # The user shouldn't be able to delete themselves.
        # The UI should prevent this from happening, but return a 500 error just in case
        if current_user.id == user_id:
            abort(500)

        # Check the user ID is actually valid
        user = User.query.filter(User.id == user_id)
        if not user.first():
            abort(404)

        # Delete all records across all tables associated with the specified user
        UserPermission.query.filter(UserPermission.user_id == user_id).delete()
        user.delete()

        # Commit deletions to database
        db.session.commit()

        flash("User has been deleted successfully.", "success")

        return redirect(url_for("admin/users"))