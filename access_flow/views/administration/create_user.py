from flask import request, render_template
from flask.views import View
from flask_login import login_required
from access_flow.forms.user import CreateUserForm

class AdministrationCreateUserView(View):
    methods = ["GET"]
    #decorators = [login_required]

    def dispatch_request(self):
        form = CreateUserForm(request.form)
        autofocus = "first_name"

        return render_template("pages/administration/create_user.html", form = form, autofocus = autofocus)