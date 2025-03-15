from flask import request, flash, redirect, url_for, abort
from flask.views import View
from flask_login import login_required, current_user
from accessflow.decorators import permission_required
from accessflow.models.service import Service
from accessflow import db

class ServiceDeleteView(View):
    methods = ["GET"]
    decorators = [login_required, permission_required("delete_services")]

    def dispatch_request(self, service_id):
        # Delete all records across all tables associated with the specified service
        service = Service.query.filter(Service.id == service_id).delete()

        # Check the service ID is actually valid
        if not service:
            abort(404)

        db.session.commit()

        flash("Service has been deleted successfully.", "success")

        return redirect(url_for("admin/services"))