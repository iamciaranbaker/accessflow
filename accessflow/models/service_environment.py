from enum import Enum
from accessflow import db

class ServiceEnvironmentType(Enum):
    NONPROD = "nonprod"
    PROD = "prod"
    UNKNOWN = "unknown"

class ServiceEnvironment(db.Model):
    # Table Name
    __tablename__ = "service_environments"

    # Columns
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), primary_key = True)
    name = db.Column(db.String(30), primary_key = True)
    type = db.Column(db.Enum(ServiceEnvironmentType))
    order = db.Column(db.Integer)

    def __init__(self, service_id, name, type, order):
        self.service_id = service_id
        self.name = name
        self.type = type
        self.order = order

    def __repr__(self):
        return f"<ServiceEnvironment(service_id=\"{self.service_id}\", name=\"{self.name}\")"