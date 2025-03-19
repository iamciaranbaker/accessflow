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
    justification = db.Column(db.Text, nullable = False)
    pid = db.Column(db.Integer)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"))
    status = db.Column(db.Enum(RequestStatus))
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Relationships
    service = db.relationship("Service", lazy = "joined")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Request(id=\"{self.id}\", name=\"{self.name}\")"