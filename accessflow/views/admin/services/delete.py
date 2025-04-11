from flask import request, flash, redirect, url_for, abort
from flask.views import View
from flask_login import login_required, current_user
from accessflow.decorators import permission_required
from accessflow.models.request_service import RequestService
from accessflow.models.service import Service
from accessflow import db

class AdminServiceDeleteView(View):
    methods = ["GET"]
    decorators = [permission_required("delete_services"), login_required]

    def dispatch_request(self):
        # Fetch the service_id query parameter
        try:
            service_id = int(request.args.get("id"))
        except:
            abort(404)

        # Delete all records across all tables associated with the specified service
        request_services = RequestService.query.filter(RequestService.service_id == service_id).delete()
        service = Service.query.filter(Service.id == service_id).delete()

        # Check the service ID is actually valid
        if not request_services or not service:
            abort(404)

        db.session.commit()

        flash("Service has been deleted successfully.", "success")

        return redirect(url_for("admin/services"))