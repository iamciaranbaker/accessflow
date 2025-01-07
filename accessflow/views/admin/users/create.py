from flask import request, render_template
from flask.views import View
from flask_login import login_required
from accessflow.forms.user import CreateUserForm

class UserCreateView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        form = CreateUserForm(request.form)
        autofocus = "first_name"

        return render_template("pages/admin/users/create.html", form = form, autofocus = autofocus)