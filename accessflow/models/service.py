from accessflow import db

class Service(db.Model):
    # Table Name
    __tablename__ = "services"

    # Columns
    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    project_url = db.Column(db.String(250), nullable = False)
    project_access_token = db.Column(db.String(20), nullable = False)
    project_access_token_expires_at = db.Column(db.DateTime)
    supports_two_factor = db.Column(db.Boolean, default = False, nullable = False)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Override the default constructor to pass in what we need to create a user. Everything else is set as a default.
    def __init__(self, name, supports_two_factor):
        self.name = name
        self.supports_two_factor = supports_two_factor

    def __repr__(self):
        return f"<Service(id=\"{self.id}\", name=\"{self.name}\")"

    @staticmethod
    def get_all():
        return Service.query.all()