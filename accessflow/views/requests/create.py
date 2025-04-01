from flask import request, abort, flash, render_template
from flask.views import View
from accessflow.forms.request import CreateRequestForm
from accessflow.models.request import Request, RequestType
from accessflow import db

class RequestCreateView(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        request_type = request.args.get("type")
        # Check if a request type has been passed through
        if not request_type:
            return render_template("pages/requests/create.html")
        # Check the request type exists
        if request_type not in RequestType:
            abort(404)

        form = CreateRequestForm(request.form)

        if request.method == "POST":
            if form.validate_on_submit():
                sc_clearance = None
                if form.sc_clearance.data:
                    sc_clearance = form.sc_clearance.data == "true"
                    
                req = Request(
                    type = request_type,
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
            
        return render_template(f"pages/requests/create_{request_type}.html", form = form)