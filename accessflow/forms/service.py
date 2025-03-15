from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp
from accessflow import gitlab_handler
from accessflow.config import Config

class CreateServiceForm(FlaskForm):
    name = StringField("Name", [DataRequired(), Length(min = 2, max = 50), Regexp(regex = r"^[a-zA-Z\s\/\-]+$", message = "Name is invalid.")])
    project_url = StringField("Project URL", [DataRequired()])
    project_access_token = PasswordField("Project Access Token", [DataRequired()])
    auto_rotate_pat = BooleanField("Automatically rotate Project Access Token near expiration?", render_kw = {"checked": ""})
    submit = SubmitField("Create Service")

    def validate_project_url_and_access_token(self):
        project_url = self.project_url.data.replace(Config.GITLAB_URL, "")
        project_access_token = self.project_access_token.data

        scopes_to_check = ["api", "read_repository"]
        if self.auto_rotate_pat.data:
            scopes_to_check.append("self_rotate")
        
        # Placeholder for GitLab PAT verification
        if not gitlab_handler.validate_project_access_token(project_url, project_access_token, scopes = scopes_to_check):
            error = "Project URL and Project Access Token are invalid."
            # Manually add validation errors for both fields
            self.project_url.errors.append(error)
            self.project_access_token.errors.append(error)
            return False
        
        return True

    # Override validate_on_submit method to add additional custom validation
    def validate_on_submit(self, extra_validators = None):
        # Call the base validate_on_submit method first
        if not super().validate_on_submit(extra_validators = extra_validators):
            return False
        
        # Run the custom combined validation for project_url and project_access_token
        return self.validate_project_url_and_access_token()