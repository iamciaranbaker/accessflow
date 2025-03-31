from accessflow import db

class RequestService(db.Model):
    # Table Name
    __tablename__ = "request_services"

    # Columns
    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"), primary_key = True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), primary_key = True)