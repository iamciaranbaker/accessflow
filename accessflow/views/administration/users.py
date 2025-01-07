from flask import render_template
from flask.views import View
from flask_login import login_required

class AdministrationUsersView(View):
    methods = ["GET"]
    #decorators = [login_required]

    def dispatch_request(self):
        return render_template("pages/administration/users.html")