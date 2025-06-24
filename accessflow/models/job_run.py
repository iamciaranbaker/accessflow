from enum import Enum
from accessflow import db, get_db_time

class JobRunStatus(Enum):
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    RUNNING = "Running"

class JobRun(db.Model):
    # Table Name
    __tablename__ = "job_runs"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id", name = "fk_job_run_job_id"))
    status = db.Column(db.Enum(JobRunStatus), default = JobRunStatus.RUNNING)
    parameters = db.Column(db.Text)
    triggered_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    started_at = db.Column(db.DateTime, default = db.func.now())
    ended_at = db.Column(db.DateTime)

    # Relationships
    job = db.relationship("Job", foreign_keys = [job_id], back_populates = "runs", lazy = "select")
    logs = db.relationship("JobLog", lazy = "select")
    triggerer = db.relationship("User", lazy = "select")

    def __init__(self, job_id, parameters, triggered_by = None):
        self.job_id = job_id
        self.parameters = parameters
        self.triggered_by = triggered_by

    def __repr__(self):
        return f"<JobRun(id = '{self.id}', job_id = '{self.job_id}', status = '{self.status}')"
    
    def mark_as_done(self, status, session):
        self.status = status
        self.ended_at = get_db_time()
        session.commit()