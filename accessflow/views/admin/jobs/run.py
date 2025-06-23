from flask import request, abort, redirect, url_for
from flask.views import View
from flask_login import login_required, current_user
from accessflow.decorators import permission_required
from accessflow.models.job import Job

class AdminJobRunView(View):
    methods = ["GET"]
    decorators = [permission_required("run_jobs"), login_required]

    def dispatch_request(self):
        # Fetch the job_id query parameter
        job_id = request.args.get("id")

        # Fetch the job based on the ID
        job = Job.query.filter(Job.id == job_id).first()
        # If no job was found with the given ID, return a 404 error
        if not job:
            abort(404)

        # Run the job
        job_run_id = job.run(current_user.id)

        return redirect(url_for("admin/jobs/logs", id = job.id, run_id = job_run_id))