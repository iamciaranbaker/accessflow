from flask import render_template
from flask.views import View
from flask_login import login_required
from accessflow.models.request import Request

class RequestListView(View):
    methods = ["GET"]

    def dispatch_request(self):
        return render_template("pages/requests/list.html", requests = Request.query.all())