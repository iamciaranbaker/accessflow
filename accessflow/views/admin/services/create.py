from flask import request, flash, redirect, url_for, render_template
from flask.views import View
from flask_login import login_required, current_user
from accessflow.decorators import permission_required
from accessflow.forms.service import CreateServiceForm
from accessflow.models.service import Service
from accessflow import db

class ServiceCreateView(View):
    methods = ["GET", "POST"]
    decorators = [login_required, permission_required("create_services")]

    def dispatch_request(self):
        form = CreateServiceForm(request.form)

        if request.method == "POST":
            if form.validate_on_submit():
                service = Service(
                    name = form.name.data,
                )

                db.session.add(service)
                db.session.commit()

                flash("Service has been created successfully.", "success")

                return redirect(url_for("admin/services"))
            else:
                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, "danger")

        return render_template("pages/admin/services/create.html", form = form)