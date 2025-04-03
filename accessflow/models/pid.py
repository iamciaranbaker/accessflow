from enum import Enum
from accessflow import db

class PIDEnvironmentType(Enum):
    NONPROD = "nonprod"
    PROD = "prod"

class PID(db.Model):
    # Table Name
    __tablename__ = "pids"

    # Columns
    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    uid = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(100), nullable = False)
    comment = db.Column(db.String(100), nullable = False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    environment_type = db.Column(db.Enum(PIDEnvironmentType), primary_key = True)
    exists_in_gl = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Relationships
    team = db.relationship("Team", lazy = "joined")

    def __init__(self, uid, name, comment, team_id, environment_type):
        self.uid = uid
        self.name = name
        self.comment = comment
        self.team_id = team_id
        self.environment_type = environment_type

    def __repr__(self):
        return f"<PID(id=\"{self.id}\", uid=\"{self.uid}\", name=\"{self.name}\", comment=\"{self.comment}\")"