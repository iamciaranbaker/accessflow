from flask import request, flash, redirect, url_for, render_template
from flask.views import View
from flask_login import login_required
from datetime import datetime
from accessflow.decorators import permission_required
from accessflow.forms.service import CreateServiceForm
from accessflow.models.service import Service
from accessflow import db, gitlab_handler

class ServiceCreateView(View):
    methods = ["GET", "POST"]
    decorators = [login_required, permission_required("create_services")]

    def dispatch_request(self):
        form = CreateServiceForm(request.form)

        if request.method == "POST":
            if form.validate_on_submit():
                token = gitlab_handler.get_project_access_token(form.project_access_token.data)
                service = Service(
                    name = form.name.data,
                    gl_project_url = gitlab_handler.sanitize_project_url(form.project_url.data, url_encode = False),
                    gl_project_access_token = form.project_access_token.data,
                    gl_project_access_token_auto_rotate = form.auto_rotate_pat.data
                )
                service.set_gl_project_access_token_id(token["id"])
                service.set_gl_project_access_token_expires_at(token["expires_at"])

                db.session.add(service)
                db.session.commit()

                flash("Service has been created successfully.", "success")

                return redirect(url_for("admin/services"))
            else:
                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, "danger")

        return render_template("pages/admin/services/create.html", form = form)