from flask import request, render_template
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.pid import PID

class PIDListView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        pids = PID.query.paginate(per_page = None if request.args.get("per_page") else 10, max_per_page = 30)
        return render_template("pages/pids/list.html", pids = pids)