from enum import Enum
from accessflow.models.service import Service
from accessflow.models.pid import PID, PIDEnvironmentType
from accessflow.models.request_pid import RequestPID
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
    name = db.Column(db.String(100), nullable = False)
    team = db.Column(db.Integer)
    nonprod_pid = db.Column(db.String(20))
    nonprod_ssh_key = db.Column(db.Text)
    prod_pid = db.Column(db.String(20))
    prod_ssh_key = db.Column(db.Text)
    sc_clearance = db.Column(db.Boolean)
    justification = db.Column(db.Text)
    status = db.Column(db.Enum(RequestStatus), default = RequestStatus.PENDING)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Relationships
    services = db.relationship("Service", secondary = "request_services", lazy = "joined")
    pids = db.relationship("RequestPID", back_populates = "request", lazy = "joined")

    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __repr__(self):
        return f"<Request(id=\"{self.id}\")"

    @property
    def nonprod_pids(self):
        return sorted(
            [pid for pid in self.pids if pid.pid.environment_type == PIDEnvironmentType.NONPROD],
            key = lambda pid: pid.confidence or 0,
            reverse = True
        )
    
    @property
    def prod_pids(self):
        return sorted(
            [pid for pid in self.pids if pid.pid.environment_type == PIDEnvironmentType.PROD],
            key = lambda pid: pid.confidence or 0,
            reverse = True
        )
    
    def add_service(self, service_id):
        service = Service.query.filter(Service.id == service_id).first()
        if not service:
            raise ValueError(f"Service with ID '{service_id}' does not exist.")
        if service not in self.services:
            self.services.append(service)
            db.session.commit()

    def add_pid(self, pid_id, confidence):
        pid = PID.query.filter(PID.id == pid_id).first()
        if not pid:
            raise ValueError(f"PID with ID '{pid_id}' does not exist.")
        if pid not in self.pids:
            db.session.add(
                RequestPID(
                    request_id = self.id,
                    pid_id = pid_id,
                    confidence = confidence
                )
            )
            db.session.commit()