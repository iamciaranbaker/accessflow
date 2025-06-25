from flask import request, flash, redirect, url_for, render_template
from flask.views import View
from flask_login import login_required, current_user
from accessflow.decorators import permission_required
from accessflow.forms.service import CreateServiceForm
from accessflow.models.service import Service
from accessflow.models.job import Job
from accessflow.models.activity_log import ActivityLog
from accessflow.gitlab.gitlab_utils import sanitize_project_url
from accessflow import db, gitlab_handler

class AdminServiceCreateView(View):
    methods = ["GET", "POST"]
    decorators = [permission_required("create_services"), login_required]

    def dispatch_request(self):
        form = CreateServiceForm(request.form)

        if request.method == "POST":
            if form.validate_on_submit():
                # Fetch token details to add to database.
                # No need to validate as the form validation should have already done this
                token = gitlab_handler.get_project_access_token(form.project_access_token.data)

                service = Service(
                    name = form.name.data,
                    gl_project_url = sanitize_project_url(form.project_url.data, url_encode = False),
                    gl_project_access_token = form.project_access_token.data,
                    gl_project_access_token_id = token["id"],
                    gl_project_access_token_auto_rotate = form.auto_rotate_pat.data,
                    gl_project_access_token_expires_at = token["expires_at"]
                )

                # Ensure the project's pipeline variables are valid
                is_valid, error = service.validate_gl_project()
                if not is_valid:
                    flash(error, "danger")
                    return render_template("pages/admin/services/create.html", form = form)
                
                db.session.add(service)
                db.session.commit()

                db.session.add(ActivityLog(
                    "service_create",
                    target = service,
                    user = current_user
                ))
                db.session.commit()

                # Kick off background job to fetch service details from GitLab.
                # This might take a few seconds so do it in the background to prevent hang for the user
                Job.query.filter(Job.name == "fetch_service_details_from_gl").first().run(
                    service_id = service.id
                )

                flash("Service has been created successfully.", "success")

                return redirect(url_for("admin/services"))
            else:
                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, "danger")

        return render_template("pages/admin/services/create.html", form = form)