from accessflow import db, gitlab_handler
import yaml

class Service(db.Model):
    # Table Name
    __tablename__ = "services"

    # Columns
    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    gl_project_url = db.Column(db.String(250), nullable = False)
    gl_project_access_token = db.Column(db.String(50), nullable = False)
    gl_project_access_token_id = db.Column(db.Integer, unique = True, nullable = False)
    gl_project_access_token_active = db.Column(db.Boolean, default = True, nullable = False)
    gl_project_access_token_auto_rotate = db.Column(db.Boolean, nullable = False)
    gl_project_access_token_expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Relationships
    environments = db.relationship("ServiceEnvironment", lazy = "select")
    host_groups = db.relationship("ServiceHostGroup", lazy = "select")

    def __init__(self, name, gl_project_url, gl_project_access_token, gl_project_access_token_id, gl_project_access_token_auto_rotate, gl_project_access_token_expires_at):
        self.name = name
        self.gl_project_url = gl_project_url
        self.gl_project_access_token = gl_project_access_token
        self.gl_project_access_token_id = gl_project_access_token_id
        self.gl_project_access_token_auto_rotate = gl_project_access_token_auto_rotate
        self.gl_project_access_token_expires_at = gl_project_access_token_expires_at

    def __repr__(self):
        return f"<Service(id = '{self.id}', name = '{self.name}', gl_project_url = '{self.gl_project_url}')"
    
    def get_pipeline_variables(self):
        gitlab_ci_file = gitlab_handler.get_project_repository_file(self.gl_project_url, self.gl_project_access_token, ".gitlab-ci.yml")
        if not gitlab_ci_file:
            return None
        
        gitlab_ci_file = yaml.safe_load(gitlab_ci_file)
        if not "variables" in gitlab_ci_file:
            return None
        
        return gitlab_ci_file["variables"]
    
    def validate_gl_project(self):
        # Check the support_users segment exists
        if not gitlab_handler.get_project_repository_tree(self.gl_project_url, self.gl_project_access_token, "ansible/support_users"):
            return False, "The project's structure is not in the expected format."
        group_vars = gitlab_handler.get_project_repository_tree(self.gl_project_url, self.gl_project_access_token, "ansible/support_users/group_vars")
        # Check the support_users segment has a group_vars folder
        if not group_vars:
            return False, "The project's structure is not in the expected format."
        pipeline_variables = self.get_pipeline_variables()
        # Check ENV_TYPE is a valid pipeline variable and has options
        if "ENV_TYPE" not in pipeline_variables or "options" not in pipeline_variables["ENV_TYPE"]:
            return False, "The project's pipeline variables are not in the expected format."
        # Check HOST_GROUP is a valid pipeline variable and has options
        if "HOST_GROUP" not in pipeline_variables or "options" not in pipeline_variables["HOST_GROUP"]:
            return False, "The project's pipeline variables are not in the expected format."
        # Fetch all file names from group_vars without the .yml file extension
        group_vars = {item["name"].replace(".yml", "") for item in group_vars}
        # Check if HOST_GROUP options are present in group_vars
        for host_group in pipeline_variables["HOST_GROUP"]["options"]:
            if host_group not in group_vars:
                return False, "The project's structure is not in the expected format."
        return True, ""