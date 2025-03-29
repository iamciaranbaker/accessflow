from flask import render_template
from flask.views import View
from flask_login import login_required
from accessflow.models.request import Request
from accessflow.models.pid import PID
from accessflow.models.team import Team
from accessflow.models.service import Service

class AdminIndexView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        counts = {
            "requests": Request.query.count(),
            "pids": PID.query.count(),
            "teams": Team.query.count(),
            "services": Service.query.count()
        }
        return render_template("pages/admin/dashboard.html", counts = counts)