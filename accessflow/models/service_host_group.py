from accessflow import db

class ServiceHostGroup(db.Model):
    # Table Name
    __tablename__ = "service_host_groups"

    # Columns
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), primary_key = True)
    name = db.Column(db.String(30), primary_key = True)
    order = db.Column(db.Integer)

    def __init__(self, service_id, name, order):
        self.service_id = service_id
        self.name = name
        self.order = order

    def __repr__(self):
        return f"<ServiceHostGroup(service_id = '{self.service_id}', name = '{self.name}')"