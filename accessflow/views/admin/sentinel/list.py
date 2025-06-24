from flask import request, redirect, url_for, render_template
from flask.views import View
from flask_login import login_required
from sqlalchemy.orm import joinedload
from accessflow.models.activity_log import ActivityLog
from accessflow.models.activity_event_type import ActivityEventType

class AdminSentinelListView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        activity_logs = ActivityLog.query.options(joinedload(ActivityLog.event_type)).join(ActivityEventType)

        # Check if a search query parameter is present
        search = request.args.get("q")
        # Check if search query parameter is empty, i.e. empty search field submitted
        if search is not None and not search.strip():
            # Redirect to base PIDs page for cleaner URL
            return redirect(url_for("admin/sentinel"))
        if search:
            # Allow the query to search for anything containing the search term
            search = f"%{search}%"
            # Filter against user name
            activity_logs = activity_logs.filter(
                ActivityLog.user.first_name.like(search) |
                ActivityLog.user.last_name.like(search)
            )

        # Check if a filter has been applied for event type
        filtered_event_types = request.args.getlist("filter[event_type]")
        if filtered_event_types:
            activity_logs = activity_logs.filter(ActivityEventType.name.in_(filtered_event_types))
        
        activity_logs = activity_logs.order_by(ActivityLog.created_at.desc())
        # Paginate the returned activity logs
        activity_logs = activity_logs.paginate(per_page = None if request.args.get("per_page") else 8, max_per_page = 30)

        # Create map of filtering options
        filter_options = {
            "event_types": [{"value": event_type.name, "label": event_type.friendly_name} for event_type in ActivityEventType.query.all()]
        }

        return render_template("pages/admin/sentinel/list.html", activity_logs = activity_logs, filter_options = filter_options)