from accessflow import db

class Team(db.Model):
    # Table Name
    __tablename__ = "teams"

    # Columns
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    exists_in_gl = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Team(id=\"{self.id}\", name=\"{self.name}\")"