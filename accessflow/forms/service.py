from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class CreateServiceForm(FlaskForm):
    name = StringField("Name", [DataRequired(), Length(min = 2, max = 50), Regexp(regex = r"^[a-zA-Z\s\/\-]+$", message = "Name is invalid.")])
    project_url = StringField("Project URL", [DataRequired()])
    project_access_token = PasswordField("Project Access Token", [DataRequired()])
    submit = SubmitField("Create Service")

    def validate_project_url_and_access_token(self):
        project_url = self.project_url.data
        project_access_token = self.project_access_token.data
        
        # Placeholder for GitLab PAT verification
        if True:
            # Manually add validation errors for both fields
            self.project_url.errors.append("Project URL and Project Access Token are invalid.")
            self.project_access_token.errors.append("Project URL and Project Access Token are invalid.")
            return False
        
        return True

    # Override validate_on_submit method to add additional custom validation
    def validate_on_submit(self, extra_validators = None):
        # Call the base validate_on_submit method first
        if not super().validate_on_submit(extra_validators = extra_validators):
            return False
        
        # Run the custom combined validation for project_url and project_access_token
        return self.validate_project_url_and_access_token()