from flask import render_template
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.user import User

class AdminUserListView(View):
    methods = ["GET"]
    decorators = [permission_required("list_users"), login_required]

    def dispatch_request(self):
        return render_template("pages/admin/users/list.html", users = User.get_all())