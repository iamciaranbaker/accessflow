from flask import render_template, abort
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.job import Job
from accessflow.models.job_run import JobRun, JobRunStatus
from accessflow.models.job_log import JobLog

class JobLogsView(View):
    methods = ["GET"]
    decorators = [permission_required("list_jobs"), login_required]

    def dispatch_request(self, job_id):
        job = Job.query.filter(Job.id == job_id).first()
        if not job:
            abort(404)

        previous_runs = JobRun.query.filter(JobRun.job_id == job_id, JobRun.status != JobRunStatus.RUNNING).order_by(JobRun.started_at.desc()).limit(5).all()

        return render_template("pages/admin/jobs/logs.html", job = job, previous_runs = previous_runs)