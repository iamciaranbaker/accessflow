from enum import Enum
from accessflow import db

class PIDEnvironmentType(Enum):
    COMBINED = "combined"
    NONPROD_ONLY = "nonprod_only"
    PROD_ONLY = "prod_only"

class PID(db.Model):
    # Table Name
    __tablename__ = "pids"

    # Columns
    uid = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(100), nullable = False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    environment_type = db.Column(db.Enum(PIDEnvironmentType), primary_key = True)
    exists_in_gl = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Relationships
    team = db.relationship("Team", lazy = "joined")

    def __init__(self, uid, name, team_id, environment_type):
        self.uid = uid
        self.name = name
        self.team_id = team_id
        self.environment_type = environment_type

    def __repr__(self):
        return f"<PID(uid=\"{self.uid}\", name=\"{self.name}\")"
    
    @staticmethod
    def get_all():
        return PID.query.all()