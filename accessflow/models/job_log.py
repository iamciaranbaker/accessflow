from sqlalchemy.dialects.mysql import TIMESTAMP
from accessflow import db
import logging

class JobLogHandler(logging.Handler):
    def __init__(self, job_run_id, session):
        super().__init__()
        self.job_run_id = job_run_id
        self.session = session

    def emit(self, record):
        log_message = self.format(record)
        try:
            self.session.add(JobLog(
                job_run_id = self.job_run_id,
                level = record.levelname,
                message = log_message
            ))
            self.session.commit()
        except Exception:
            return

class JobLog(db.Model):
    # Table Name
    __tablename__ = "job_logs"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    job_run_id = db.Column(db.Integer, db.ForeignKey("job_runs.id"))
    level = db.Column(db.String(10))
    message = db.Column(db.Text)
    created_at = db.Column(TIMESTAMP(fsp = 6), default = db.func.now(6))

    def __init__(self, job_run_id, level, message):
        self.job_run_id = job_run_id
        self.level = level
        self.message = message

    def __repr__(self):
        return f"<JobLog(id=\"{self.id}\")"