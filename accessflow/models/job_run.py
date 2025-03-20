from enum import Enum
from accessflow import db

class JobRunStatus(Enum):
    SUCCESSFUL = "Successful"
    FAILED = "Failed"
    RUNNING = "Running"

class JobRun(db.Model):
    # Table Name
    __tablename__ = "job_runs"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    status = db.Column(db.Enum(JobRunStatus), default = JobRunStatus.RUNNING)
    triggered_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    started_at = db.Column(db.DateTime, default = db.func.now())
    ended_at = db.Column(db.DateTime)

    # Relationships
    logs = db.relationship("JobLog", lazy = "joined")

    def __init__(self, job_id):
        self.job_id = job_id

    def __repr__(self):
        return f"<JobRun(id=\"{self.id}\")"
    
    def mark_as_done(self, status):
        self.status = status
        self.ended_at = db.session.query(db.func.now()).scalar()
        db.session.commit()