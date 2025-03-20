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
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"))
    justification = db.Column(db.Text, nullable = False)
    status = db.Column(db.Enum(RequestStatus), default = RequestStatus.PENDING)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Relationships
    service = db.relationship("Service", lazy = "joined")

    def __init__(self, pid, service_id, justification):
        self.pid = pid
        self.service_id = service_id
        self.justification = justification

    def __repr__(self):
        return f"<Request(id=\"{self.id}\", pid=\"{self.pid}\", service=\"{self.service}\")"
    
    @staticmethod
    def get_all():
        return Request.query.all()