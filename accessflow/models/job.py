from enum import Enum
from datetime import datetime
from croniter import croniter
from accessflow.logger import logger
from accessflow import db
import importlib

class JobLastRunStatus(Enum):
    SUCCESSFUL = "Successful"
    FAILED = "Failed"
    RUNNING = "Running"

class Job(db.Model):
    # Table Name
    __tablename__ = "jobs"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    module_path = db.Column(db.String(100), nullable = False)
    class_name = db.Column(db.String(100), nullable = False)
    cron_expression = db.Column(db.String(30), nullable = False)
    last_run_at = db.Column(db.DateTime)
    last_run_status = db.Column(db.Enum(JobLastRunStatus))
    next_run_at = db.Column(db.DateTime)

    def __init__(self, name, module_path, class_name, cron_expression):
        self.name = name
        self.module_path = module_path
        self.class_name = class_name
        self.cron_expression = cron_expression
        self.next_run_at = self.get_next_run_at()

    def __repr__(self):
        return f"<Job(id=\"{self.id}\", name=\"{self.name}\", module_path=\"{self.module_path}\", class_name=\"{self.class_name}\")"
    
    def mark_as_complete(self):
        self.last_run_at = db.func.now()
        self.last_run_status = JobLastRunStatus.SUCCESSFUL
        self.next_run_at = self.get_next_run_at()
        db.session.commit()

    def get_next_run_at(self):
        return croniter(self.cron_expression, db.session.query(db.func.now()).scalar()).get_next(datetime)

    def run(self):
        try:
            job_module = importlib.import_module(self.module_path)
            job_class = getattr(job_module, self.class_name)

            job_instance = job_class()
            job_instance.run()
        except ModuleNotFoundError:
            raise ValueError(f"Module {self.module_path} not found.")
        except AttributeError:
            raise ValueError(f"Class {self.class_name} not found in module {self.module_path}.")
        
        self.mark_as_complete()
    
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