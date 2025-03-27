from flask import render_template
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.team import Team

class TeamListView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        return render_template("pages/teams/list.html", teams = Team.query.all())