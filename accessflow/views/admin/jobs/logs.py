from flask import request, render_template, abort
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.job import Job
from accessflow.models.job_run import JobRun, JobRunStatus
import json

class AdminJobLogsView(View):
    methods = ["GET"]
    decorators = [permission_required("list_jobs"), login_required]

    def dispatch_request(self):
        # Fetch the job_id query parameter
        job_id = request.args.get("id")
        # Fetch the job_run_id query parameter - if not set, it will default to the latest run
        job_run_id = request.args.get("run_id")

        # Fetch the job based on the ID
        job = Job.query.filter(Job.id == job_id).first()
        # If no job was found with the given ID, return a 404 error
        if not job:
            abort(404)

        if job_run_id:
            # Fetch the job run based on the ID
            job_run = JobRun.query.filter(JobRun.id == job_run_id, JobRun.job_id == job_id, JobRun.status != JobRunStatus.RUNNING).order_by(JobRun.started_at.desc()).first()
        else:
            # Fetch the latest job run for the given job ID that isn't still running
            job_run = JobRun.query.filter(JobRun.job_id == job_id, JobRun.status != JobRunStatus.RUNNING).order_by(JobRun.started_at.desc()).first()

        # If no job run was found with the given ID, return a 404 error
        if not job_run:
            abort(404)

        # Get the actual job run ID from the returned object
        job_run_id = job_run.id

        parameters = json.loads(job_run.parameters)

        # Get 5 of the previous completed runs
        previous_runs = JobRun.query.filter(JobRun.job_id == job.id, JobRun.status != JobRunStatus.RUNNING, JobRun.id != job_run_id).order_by(JobRun.started_at.desc()).limit(5).all()

        return render_template("pages/admin/jobs/logs.html", job_run = job_run, parameters = parameters, previous_runs = previous_runs)