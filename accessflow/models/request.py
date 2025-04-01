from enum import Enum
from accessflow.models.pid import PID, PIDEnvironmentType
from accessflow.models.service import Service
from accessflow import db

class RequestType(Enum):
    ACCOUNT_CREATION = "account_creation"
    SERVICE_ACCESS = "service_access"
    MFA_RESET = "mfa_reset"

class RequestStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"

class Request(db.Model):
    # Table Name
    __tablename__ = "requests"

    # Columns
    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    type = db.Column(db.Enum(RequestType))
    name = db.Column(db.String(100))
    nonprod_pid_uid = db.Column(db.Integer)
    prod_pid_uid = db.Column(db.Integer)
    sc_clearance = db.Column(db.Boolean)
    justification = db.Column(db.Text, nullable = False)
    status = db.Column(db.Enum(RequestStatus), default = RequestStatus.PENDING)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Relationships
    services = db.relationship("Service", secondary = "request_services", lazy = "joined")

    def __init__(self, type, name, sc_clearance, justification, nonprod_pid_uid = None, prod_pid_uid = None):
        self.type = type
        self.name = name
        self.sc_clearance = sc_clearance
        self.justification = justification
        self.nonprod_pid_uid = nonprod_pid_uid
        self.prod_pid_uid = prod_pid_uid

    def __repr__(self):
        return f"<Request(id=\"{self.id}\", nonprod_pid=\"{self.nonprod_pid}\", prod_pid=\"{self.prod_pid}\")"
    
    def add_service(self, service_id):
        service = Service.query.filter(Service.id == service_id).first()
        if not service:
            raise ValueError(f"Service with ID '{service_id}' does not exist.")
        if service not in self.services:
            self.services.append(service)
            db.session.commit()