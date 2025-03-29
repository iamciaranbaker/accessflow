from flask import render_template
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.service import Service

class AdminServiceListView(View):
    methods = ["GET"]
    decorators = [permission_required("list_services"), login_required]

    def dispatch_request(self):
        return render_template("pages/admin/services/list.html", services = Service.get_all())