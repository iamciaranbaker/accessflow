from flask import request, abort, redirect, url_for, render_template
from flask.views import View
from flask_login import login_required
from accessflow.models.request import Request
from accessflow.models.service_environment import ServiceEnvironment
from accessflow.models.service_host_group import ServiceHostGroup
from accessflow.models.service_host_group_team import ServiceHostGroupTeam
from accessflow import db

class AdminRequestListView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        request_id = request.args.get("id")
        # Check if a request ID query parameter has been passed 
        if request_id:
            # Fetch the request based on the ID
            requesto = Request.query.filter(Request.id == request_id).first()
            # If no request was found with the given ID, return a 404 error
            if not requesto:
                abort(404)

            service_matches = []

            # Iterate through each service in the request
            for service in requesto.services:
                service_match = {
                    "name": service.name,
                    "nonprod": {
                        "environments": [],
                        "host_groups": []
                    },
                    "prod": {
                        "environments": [],
                        "host_groups": []
                    }
                }
                for pid in requesto.pids:
                    # Get all environments associated with the service
                    environments = ServiceEnvironment.query.filter(ServiceEnvironment.service_id == service.id, ServiceEnvironment.type == pid.pid.environment_type.value).order_by(ServiceEnvironment.order.asc()).all()
                    for environment in environments:
                        service_match[pid.pid.environment_type.value]["environments"].append({
                            "name": environment.name,
                            "pid_id": pid.pid_id
                        })
                    # Get all host groups associated with the service as well as the matched PID's team
                    host_groups = (
                        db.session.query(ServiceHostGroup)
                        .join(ServiceHostGroupTeam, (ServiceHostGroup.service_id == ServiceHostGroupTeam.service_id) & (ServiceHostGroup.name == ServiceHostGroupTeam.name))
                        .filter(ServiceHostGroup.service_id == service.id, ServiceHostGroupTeam.team_id == pid.pid.team_id)
                        .order_by(ServiceHostGroup.order.asc())
                        .all()
                    )
                    for host_group in host_groups:
                        if host_group.name not in service_match[pid.pid.environment_type.value]["host_groups"]:
                            service_match[pid.pid.environment_type.value]["host_groups"].append({
                                "name": host_group.name,
                                "pid_id": pid.pid_id
                            })
                service_matches.append(service_match)

            return render_template("pages/admin/requests/view.html", requesto = requesto, service_matches = service_matches)

        requests = Request.query

        # Check if a search query parameter is present
        search = request.args.get("q")
        # Check if search query parameter is empty, i.e. empty search field submitted
        if search is not None and not search.strip():
            # Redirect to base requests page for cleaner URL
            return redirect(url_for("admin/requests"))
        if search:
            # Allow the query to search for anything containing the search term
            search = f"%{search}%"
            # Filter against name
            requests = requests.filter(
                Request.name.like(search)
            )

        # Check if a filter has been applied for type
        filtered_types = request.args.getlist("filter[type]")
        if filtered_types:
            requests = requests.filter(Request.type.in_(filtered_types))

        # Check if a filter has been applied for status
        filtered_statuses = request.args.getlist("filter[status]")
        if filtered_statuses:
            requests = requests.filter(Request.status.in_(filtered_statuses))

        # Order requests by created date
        requests = requests.order_by(Request.created_at.desc())

        # Paginate the returned requests
        requests = requests.paginate(per_page = None if request.args.get("per_page") else 8, max_per_page = 30)

        # Create map of filtering options
        filter_options = {
            "types": [
                {
                    "value": "account_creation",
                    "label": "Account Creation"
                },
                {
                    "value": "service_access",
                    "label": "Service Access"
                },
                {
                    "value": "mfa_reset",
                    "label": "MFA Reset"
                }
            ],
            "statuses": [
                {
                    "value": "pending",
                    "label": "Pending"
                },
                {
                    "value": "approved",
                    "label": "Approved"
                },
                {
                    "value": "declined",
                    "label": "Declined"
                }
            ]
        }

        return render_template("pages/admin/requests/list.html", requests = requests, filter_options = filter_options)