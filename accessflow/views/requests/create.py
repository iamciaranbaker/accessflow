from flask import request, abort, flash, render_template, redirect, url_for
from flask.views import View
from accessflow.forms.request import AccountCreationRequestForm, ServiceAccessRequestForm
from accessflow.models.request import Request, RequestType
from accessflow import db

class RequestCreateView(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        request_type = request.args.get("type")
        # Check if a request type has been passed through.
        # If it hasn't, then return the page listing the different request types
        if not request_type:
            return render_template("pages/requests/create.html")

        match request_type:
            case "account_creation":
                form = AccountCreationRequestForm(request.form)
            case "service_access":
                form = ServiceAccessRequestForm(request.form)
            case _:
                # Anything else (not a valid request type), return 404
                abort(404)

        if request.method == "POST":
            if form.validate_on_submit():
                sc_clearance = None
                if form.sc_clearance.data:
                    sc_clearance = form.sc_clearance.data == "true"
                    
                req = Request(
                    type = request_type,
                    name = form.name.data
                )
                req.sc_clearance = sc_clearance
                req.nonprod_pid_uid = 8904064
                req.prod_pid_uid = 8904064

                if request_type == "account_creation":
                    req.nonprod_ssh_key = form.nonprod_ssh_key.data
                    req.prod_ssh_key = form.prod_ssh_key.data
                elif request_type == "service_access":
                    for service_id in form.services.data:
                        req.add_service(service_id)
                    req.justification = form.justification.data

                db.session.add(req)
                db.session.commit()

                flash("Request has been created successfully.", "success")

                return redirect(url_for("requests"))
            else:
                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, "danger")
            
        return render_template(f"pages/requests/create_{request_type}.html", form = form)