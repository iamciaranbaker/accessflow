from datetime import timedelta
from accessflow import db
import importlib

class Job(db.Model):
    # Table Name
    __tablename__ = "jobs"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    module_path = db.Column(db.String(100), nullable = False)
    class_name = db.Column(db.String(100), nullable = False)
    run_interval = db.Column(db.Integer, nullable = False)
    last_run_at = db.Column(db.DateTime, default = db.func.now())
    next_run_at = db.Column(db.DateTime, default = db.func.now())

    def __init__(self, name, module_path, class_name, run_interval):
        self.name = name
        self.module_path = module_path
        self.class_name = class_name
        self.run_interval = run_interval

    def __repr__(self):
        return f"<Job(id=\"{self.id}\", name=\"{self.name}\", module_path=\"{self.module_path}\", class_name=\"{self.class_name}\")"
    
    def mark_as_complete(self):
        self.last_run_at = db.func.now()
        self.next_run_at = db.session.query(db.func.now()).scalar() + timedelta(seconds = self.run_interval)
        db.session.commit()

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
            Job("check_gl_project_access_tokens", "accessflow.jobs.check_gl_project_access_tokens", "CheckGLProjectAccessTokens", 1),
            Job("rotate_gl_project_access_tokens", "accessflow.jobs.rotate_gl_project_access_tokens", "RotateGLProjectAccessTokens", 5)
        ]

        for job in jobs:
            existing_job = Job.query.filter(Job.name == job.name).first()
            if existing_job:
                existing_job.module_path = job.module_path
                existing_job.class_name = job.class_name
                existing_job.run_interval = job.run_interval
                print(f"Updated {existing_job}")
            else:
                db.session.add(job)
                print(f"Created {job}")

        db.session.commit()

    @staticmethod
    def run_all():
        jobs = Job.query.filter(Job.next_run_at < db.func.now()).all()
        
        for job in jobs:
            print(f"Running {job}")
            job.run()