from flask import request, flash, render_template
from flask.views import View
from accessflow.forms.request import CreateRequestForm
from accessflow.models.request import Request
from accessflow import db

class RequestCreateView(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = CreateRequestForm(request.form)

        if request.method == "POST":
            if form.validate_on_submit():
                sc_clearance = None
                if form.sc_clearance.data:
                    sc_clearance = form.sc_clearance.data == "true"
                    
                req = Request(
                    name = form.name.data,
                    sc_clearance = sc_clearance,
                    justification = form.justification.data,
                    nonprod_pid_uid = 8904064,
                    prod_pid_uid = 8904064
                )

                for service_id in form.services.data:
                    req.add_service(service_id)

                db.session.add(req)
                db.session.commit()

                flash("Request has been created successfully.", "success")
            else:
                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, "danger")
            
        return render_template("pages/requests/create_service_access.html", form = form)