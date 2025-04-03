from flask import request, abort, render_template
from flask.views import View
from flask_login import login_required
from accessflow.models.request import Request

class AdminRequestListView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        req_id = request.args.get("id")
        if not req_id:
            return render_template("pages/admin/requests/list.html", requests = Request.query.all())
        req = Request.query.filter(Request.id == req_id).first()
        if not req:
            abort(404)
        return render_template("pages/admin/requests/view.html", req = req)