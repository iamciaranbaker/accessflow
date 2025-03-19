from accessflow import db

class PID(db.Model):
    # Table Name
    __tablename__ = "pids"

    # Columns
    uid = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(100), nullable = False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    exists_in_gl = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Relationships
    team = db.relationship("Team", lazy = "joined")

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def __repr__(self):
        return f"<PID(uid=\"{self.uid}\", name=\"{self.name}\")"