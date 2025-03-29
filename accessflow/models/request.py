from enum import Enum
from accessflow import db

class RequestStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"

class Request(db.Model):
    # Table Name
    __tablename__ = "requests"

    # Columns
    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    pid = db.Column(db.Integer)
    justification = db.Column(db.Text, nullable = False)
    status = db.Column(db.Enum(RequestStatus), default = RequestStatus.PENDING)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    def __init__(self, pid, justification):
        self.pid = pid
        self.justification = justification

    def __repr__(self):
        return f"<Request(id=\"{self.id}\", pid=\"{self.pid}\")"
    
    @staticmethod
    def get_all():
        return Request.query.all()