from flask import render_template
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.job import Job

class AdminJobListView(View):
    methods = ["GET"]
    decorators = [permission_required("list_jobs"), login_required]

    def dispatch_request(self):
        return render_template("pages/admin/jobs/list.html", jobs = Job.get_all())