from flask import request, flash, redirect, url_for, render_template
from flask.views import View
from flask_login import login_required, current_user
from accessflow.decorators import permission_required
from accessflow.forms.user import CreateUserForm
from accessflow.models.user import User
from accessflow import db

class AdminUserCreateView(View):
    methods = ["GET", "POST"]
    decorators = [permission_required("create_users"), login_required]

    def dispatch_request(self):
        form = CreateUserForm(request.form)

        if request.method == "POST":                         
            if form.validate_on_submit():
                user = User(
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    email_address = form.email_address.data,
                    password = form.password.data,
                    password_reset_required = form.force_password_reset.data
                )

                # Iterate through all permission groups
                for permission_group in form.permission_groups:
                    # Iterate through all permissions inside permission group
                    for permission in permission_group["permissions"]:
                        permission, field = permission["permission"], permission["field"]

                        # Check if current user has permission, if not then skip as they can't grant a permission they don't have themselves
                        if not current_user.has_permission(permission.name):
                            continue

                        # Flask Form doesn't return permission data properly as its generated dynamically, so use request.form instead
                        if request.form[getattr(field, "name")] == "true":
                            user.add_permission(permission.name)

                db.session.add(user)
                db.session.commit()

                flash("User has been created successfully.", "success")

                return redirect(url_for("admin/users"))
            else:
                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, "danger")

        return render_template("pages/admin/users/create.html", form = form)