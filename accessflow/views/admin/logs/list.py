from flask import render_template
from flask.views import View
from flask_login import login_required
from accessflow.models.activity_log import ActivityLog

class AdminLogsListView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        activity_logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(100).all()
        return render_template("pages/admin/logs/list.html", activity_logs = activity_logs)