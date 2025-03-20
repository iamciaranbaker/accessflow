from datetime import datetime
from croniter import croniter
from accessflow.models.job_run import JobRun, JobRunStatus
from accessflow.models.job_log import JobLogHandler
from accessflow import logger, db
import importlib
import logging

class Job(db.Model):
    # Table Name
    __tablename__ = "jobs"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    module_path = db.Column(db.String(100), nullable = False)
    class_name = db.Column(db.String(100), nullable = False)
    cron_expression = db.Column(db.String(30), nullable = False)
    next_run_at = db.Column(db.DateTime, default = db.func.now())

    # Relationships
    runs = db.relationship("JobRun", lazy = "joined")

    def __init__(self, name, module_path, class_name, cron_expression):
        self.name = name
        self.module_path = module_path
        self.class_name = class_name
        self.cron_expression = cron_expression
        #self.next_run_at = self.calculate_next_run()

    def __repr__(self):
        return f"<Job(id=\"{self.id}\", name=\"{self.name}\", module_path=\"{self.module_path}\", class_name=\"{self.class_name}\")"
    
    @property
    def last_run(self):
        latest_run = JobRun.query.filter(JobRun.job_id == self.id).order_by(JobRun.started_at.desc()).first()
        return latest_run

    def calculate_next_run(self):
        return croniter(self.cron_expression, db.session.query(db.func.now()).scalar()).get_next(datetime)

    def run(self):
        # Set the job's next run time
        self.next_run_at = self.calculate_next_run()
        db.session.commit()

        # Create a new job run
        job_run = JobRun(job_id = self.id)
        db.session.add(job_run)
        db.session.commit()

        # Create a new logger for the job
        job_logger = logging.getLogger(f"job_{job_run.id}")
        job_logger.setLevel(logging.INFO)
        job_logger.addHandler(JobLogHandler(job_run.id))

        try:
            # Find the job's module
            job_module = importlib.import_module(self.module_path)
            # Find the job's class within the module
            job_class = getattr(job_module, self.class_name)
            # Create an instance of the job's class
            job_instance = job_class(job_logger)
            # Run the job
            job_instance.run()
            # Mark the job as successful
            job_run.mark_as_done(JobRunStatus.SUCCESSFUL)
        except Exception as exception:
            job_logger.critical(f"An exception occured: {exception}")
            # Mark the job as failed
            job_run.mark_as_done(JobRunStatus.FAILED)
    
    @staticmethod
    def seed_all():
        jobs = [
            Job("check_gl_project_access_tokens", "accessflow.jobs.check_gl_project_access_tokens", "CheckGLProjectAccessTokens", "* * * * *"),
            Job("rotate_gl_project_access_tokens", "accessflow.jobs.rotate_gl_project_access_tokens", "RotateGLProjectAccessTokens", "* * * * *"),
            Job("fetch_teams_from_gl", "accessflow.jobs.fetch_teams_from_gl", "FetchTeamsFromGL", "* * * * *"),
            Job("fetch_pids_from_gl", "accessflow.jobs.fetch_pids_from_gl", "FetchPIDsFromGL", "* * * * *")
        ]

        for job in jobs:
            existing_job = Job.query.filter(Job.name == job.name).first()
            if existing_job:
                existing_job.module_path = job.module_path
                existing_job.class_name = job.class_name
                existing_job.cron_expression = job.cron_expression
                logger.info(f"Updating {existing_job}")
            else:
                db.session.add(job)
                logger.info(f"Creating {job}")

        db.session.commit()

    @staticmethod
    def get_all():
        return Job.query.all()

    @staticmethod
    def run_all():
        jobs = Job.query.filter(Job.next_run_at < db.func.now()).all()
        
        for job in jobs:
            logger.info(f"Running {job}")
            job.run()