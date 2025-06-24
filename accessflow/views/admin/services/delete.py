from flask import request, flash, redirect, url_for, abort
from flask.views import View
from flask_login import login_required, current_user
from accessflow.decorators import permission_required
from accessflow.models.request_service import RequestService
from accessflow.models.service_environment import ServiceEnvironment
from accessflow.models.service_host_group import ServiceHostGroup
from accessflow.models.service_host_group_team import ServiceHostGroupTeam
from accessflow.models.service import Service
from accessflow.models.activity_log import ActivityLog
from accessflow import db

class AdminServiceDeleteView(View):
    methods = ["GET"]
    decorators = [permission_required("delete_services"), login_required]

    def dispatch_request(self):
        # Fetch the id query parameter
        try:
            service_id = int(request.args.get("id"))
        except:
            abort(404)

        # Check the service ID is actually valid
        service = Service.query.filter(Service.id == service_id)
        if not service.first():
            abort(404)

        # Delete all records across all tables associated with the specified service
        RequestService.query.filter(RequestService.service_id == service_id).delete()
        ServiceEnvironment.query.filter(ServiceEnvironment.service_id == service_id).delete()
        ServiceHostGroup.query.filter(ServiceHostGroup.service_id == service_id).delete()
        ServiceHostGroupTeam.query.filter(ServiceHostGroupTeam.service_id == service_id).delete()
        service.delete()

        # Commit deletions to database
        db.session.commit()

        db.session.add(ActivityLog(
            "service_delete",
            target = service,
            user_id = current_user.id
        ))
        db.session.commit()

        flash("Service has been deleted successfully.", "success")

        return redirect(url_for("admin/services"))