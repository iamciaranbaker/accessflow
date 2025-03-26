from flask import render_template
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.pid import PID

class PIDListView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        return render_template("pages/pids/list.html", pids = PID.get_all())