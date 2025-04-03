from accessflow import db

class RequestPID(db.Model):
    # Table Name
    __tablename__ = "request_pids"

    # Columns
    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"), primary_key = True)
    pid_id = db.Column(db.Integer, db.ForeignKey("pids.id"), primary_key = True)
    confidence = db.Column(db.Integer)

    # Relationships
    request = db.relationship("Request", back_populates = "pids")
    pid = db.relationship("PID")

    def __init__(self, request_id, pid_id, confidence):
        self.request_id = request_id
        self.pid_id = pid_id
        self.confidence = confidence