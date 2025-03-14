from accessflow import db

class Service(db.Model):
    # Table Name
    __tablename__ = "services"

    # Columns
    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    gl_project_url = db.Column(db.String(250), nullable = False)
    gl_project_access_token = db.Column(db.String(20), nullable = False)
    gl_pat_expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    def __init__(self, name, gl_project_url, gl_project_access_token):
        self.name = name
        self.gl_project_url = gl_project_url
        self.gl_project_access_token = gl_project_access_token

    def __repr__(self):
        return f"<Service(id=\"{self.id}\", name=\"{self.name}\")"
    
    # Set the password to the hashed value.
    def set_gl_pat_expires_at(self, gl_pat_expires_at):
        self.gl_pat_expires_at = gl_pat_expires_at

    @staticmethod
    def get_all():
        return Service.query.all()