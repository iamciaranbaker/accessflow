from flask import current_app
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from croniter import croniter
from enum import Enum
from accessflow.models.job_run import JobRun, JobRunStatus
from accessflow.models.job_log import JobLogHandler
from accessflow import logger, db
import importlib
import logging
import threading
import traceback
import json

class JobType(Enum):
    SCHEDULE = "schedule"
    TRIGGER = "trigger"

class Job(db.Model):
    # Table Name
    __tablename__ = "jobs"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    type = db.Column(db.Enum(JobType), nullable = False)
    module_path = db.Column(db.String(100), nullable = False)
    class_name = db.Column(db.String(100), nullable = False)
    cron_expression = db.Column(db.String(30))
    next_run_at = db.Column(db.DateTime)

    # Relationships
    runs = db.relationship("JobRun", lazy = "joined")

    def __init__(self, name, type, module_path, class_name, cron_expression = None):
        self.name = name
        self.type = type
        self.module_path = module_path
        self.class_name = class_name
        self.cron_expression = cron_expression
        if type == JobType.SCHEDULE:
            self.next_run_at = self.calculate_next_run()

    def __repr__(self):
        return f"<Job(id=\"{self.id}\", name=\"{self.name}\", type=\"{self.type}\", module_path=\"{self.module_path}\", class_name=\"{self.class_name}\")"
    
    @property
    def last_run(self):
        return JobRun.query.filter(JobRun.job_id == self.id).order_by(JobRun.started_at.desc()).first()

    def calculate_next_run(self):
        return croniter(self.cron_expression, db.session.query(db.func.now()).scalar()).get_next(datetime)

    def run(self, triggered_by = None, **kwargs):
        if self.type == JobType.SCHEDULE:
            # Set the job's next run time first, regardless of if the job succeeds or fails
            self.next_run_at = self.calculate_next_run()
            db.session.commit()

        # Create a new job run object
        job_run = JobRun(
            job_id = self.id,
            parameters = json.dumps(kwargs),
            triggered_by = triggered_by
        )
        db.session.add(job_run)
        db.session.commit()

        # Capture the job run ID as the object will likely expire and it is needed later
        job_run_id = job_run.id

        # Create a new logger for the job
        job_logger = logging.getLogger(f"job_{job_run_id}")
        # Set the job logger's default log level to info
        job_logger.setLevel(logging.INFO)
        # Add the success log level to the job logger
        setattr(job_logger, "success", lambda message, *args: job_logger._log(logging.SUCCESS, message, args))
        
        # Create a copy of the module_path and class_name for use in the background job
        module_path = self.module_path
        class_name = self.class_name
        
        def run_job_in_background(app, kwargs):
            with app.app_context():
                # Create a new session that is independent of the main thread's session
                Session = scoped_session(sessionmaker(bind = db.engine))
                session = Session()

                # Add the custom log handler to the job logger and pass in the session
                job_logger.addHandler(JobLogHandler(job_run_id, session = session))

                try:
                    # Find the job's module
                    job_module = importlib.import_module(module_path)
                    # Find the job's class within the module
                    job_class = getattr(job_module, class_name)
                    # Create an instance of the job's class, passing the job's logger and the session
                    job_instance = job_class(job_logger, session)
                    # Run the job instance (this could take some time)
                    job_instance.run(**kwargs)
                    # If it completes without exception, mark as successful
                    job_logger.success("Job succeeded")
                    # Fetch a new instance of the job run object due to previous one expiring
                    job_run = session.query(JobRun).filter(JobRun.id == job_run_id).first()
                    # Mark the job as done
                    job_run.mark_as_done(JobRunStatus.SUCCEEDED, session = session)
                except Exception as exception:
                    job_logger.critical(f"An exception occurred: {exception}")
                    # Mark the job as failed
                    job_logger.error("Job failed")
                    # Fetch a new instance of the job run object due to previous one expiring
                    job_run = session.query(JobRun).filter(JobRun.id == job_run_id).first()
                    # Mark the job as done
                    job_run.mark_as_done(JobRunStatus.FAILED, session = session)
                    # Log stacktrace for internal debugging
                    logger.error(traceback.format_exc())
                finally:
                    # Remove the session instance
                    Session.remove()

        app = current_app._get_current_object()
        # Run the job in a different thread
        threading.Thread(target = lambda: run_job_in_background(app, kwargs)).start()

    @staticmethod
    def seed_all():
        jobs = [
            Job(
                name = "check_gl_project_access_tokens",
                type = JobType.SCHEDULE,
                module_path = "accessflow.jobs.check_gl_project_access_tokens",
                class_name = "CheckGLProjectAccessTokens",
                cron_expression = "* * * * *"
            ),
            Job(
                name = "rotate_gl_project_access_tokens",
                type = JobType.SCHEDULE,
                module_path = "accessflow.jobs.rotate_gl_project_access_tokens",
                class_name = "RotateGLProjectAccessTokens",
                cron_expression = "* * * * *"
            ),
            Job(
                name = "fetch_teams_from_gl",
                type = JobType.SCHEDULE,
                module_path = "accessflow.jobs.fetch_teams_from_gl",
                class_name = "FetchTeamsFromGL",
                cron_expression = "* * * * *"
            ),
            Job(
                name = "fetch_pids_from_gl",
                type = JobType.SCHEDULE,
                module_path = "accessflow.jobs.fetch_pids_from_gl",
                class_name = "FetchPIDsFromGL",
                cron_expression = "* * * * *"
            ),
            Job(
                name = "fuzzy_match_request_to_pids",
                type = JobType.TRIGGER,
                module_path = "accessflow.jobs.fuzzy_match_request_to_pids",
                class_name = "FuzzyMatchRequestToPIDs"
            )
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
    def run_all(force = False):
        jobs = Job.query.filter(Job.type == JobType.SCHEDULE)
        if not force:
            jobs = jobs.filter(Job.next_run_at < db.func.now())
        jobs = jobs.all()

        if len(jobs) == 0:
            logger.info("There are no scheduled jobs to run!")
        else:
            for job in jobs:
                logger.info(f"Running {job}")
                job.run()