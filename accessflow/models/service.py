from accessflow import db
import json

class Service(db.Model):
    # Table Name
    __tablename__ = "services"

    # Columns
    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    gl_project_url = db.Column(db.String(250), nullable = False)
    gl_pipeline_variables = db.Column(db.Text, nullable = False)
    gl_project_access_token = db.Column(db.String(20), nullable = False)
    gl_project_access_token_id = db.Column(db.Integer, unique = True, nullable = False)
    gl_project_access_token_active = db.Column(db.Boolean, default = True, nullable = False)
    gl_project_access_token_auto_rotate = db.Column(db.Boolean, nullable = False)
    gl_project_access_token_expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    @property
    def environments(self):
        return self.get_environments()
    @property
    def host_groups(self):
        return self.get_host_groups()

    def __init__(self, name, gl_project_url, gl_project_access_token, gl_project_access_token_auto_rotate):
        self.name = name
        self.gl_project_url = gl_project_url
        self.gl_project_access_token = gl_project_access_token
        self.gl_project_access_token_auto_rotate = gl_project_access_token_auto_rotate

    def __repr__(self):
        return f"<Service(id=\"{self.id}\", name=\"{self.name}\")"
    
    def get_environments(self):
        return json.loads(self.gl_pipeline_variables)["ENV_TYPE"]["options"]
    
    def get_host_groups(self):
        return json.loads(self.gl_pipeline_variables)["HOST_GROUP"]["options"]