from flask import render_template
from flask.views import View
from flask_login import login_required
from accessflow.models.request import Request

class AdminRequestListView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        return render_template("pages/admin/requests/list.html", requests = Request.get_all())