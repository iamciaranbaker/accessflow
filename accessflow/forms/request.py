from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from accessflow.models.team import Team
from accessflow.models.service import Service

class AccountCreationRequestForm(FlaskForm):
    name = StringField("Name", [DataRequired(message = "You must enter a name."), Length(min = 2, max = 50, message = "Your name is invalid.")])
    team = SelectField("Team")
    environments = SelectMultipleField("Environments", choices = [("nonprod", "Non-Production"), ("prod", "Production")])
    nonprod_pid = StringField("Non-Production PID") # Accomodate CG and U. - e.g. cg19321, u.8904064
    nonprod_ssh_key = TextAreaField("Non-Production SSH Key")
    prod_pid = StringField("Production PID") # Accomodate U. and LSS. - e.g. u.8904064, LSS.8904064
    prod_ssh_key = TextAreaField("Production SSH Key")
    sc_clearance = SelectField("Do you have active SC clearance?", choices = [("true", "Yes"), ("false", "No")], validate_choice = False)
    submit = SubmitField("Create Request")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate teams from database
        self.team.choices = [(str(team.id), team.friendly_name) for team in Team.query.all()]

class ServiceAccessRequestForm(FlaskForm):
    name = StringField("Name", [DataRequired(message = "You must enter a name."), Length(min = 2, max = 50, message = "Your name is invalid.")])
    services = SelectMultipleField("Services")
    environments = SelectMultipleField("Environments", choices = [("nonprod", "Non-Production"), ("prod", "Production")])
    nonprod_pid = StringField("Non-Production PID") # Accomodate CG and U. - e.g. cg19321, u.8904064
    prod_pid = StringField("Production PID") # Accomodate U. and LSS. - e.g. u.8904064, LSS.8904064
    sc_clearance = SelectField("Do you have active SC clearance?", choices = [("true", "Yes"), ("false", "No")], validate_choice = False)
    justification = TextAreaField("Justification", [DataRequired()])
    submit = SubmitField("Create Request")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate services from database
        self.services.choices = [(str(service.id), service.name) for service in Service.query.all()]

    # Override validate_on_submit method to add additional custom validation
    def validate_on_submit(self, extra_validators = None):
        # Call the base validate_on_submit method first
        if not super().validate_on_submit(extra_validators = extra_validators):
            return False
        
        if not self.environments.data or len(self.environments.data) < 1:
            # Manually add validation error for environments field
            self.environments.errors.append("You must select at least one environment.")
            return False
        
        if "nonprod" in self.environments.data:
            if not self.nonprod_pid.data or self.nonprod_pid.data.strip() == "":
                # Manually add validation error for nonprod_pid field
                self.nonprod_pid.errors.append("You must enter a non-production PID.")
                return False
            if not (7 <= len(self.nonprod_pid.data.strip()) <= 9):
                self.nonprod_pid.errors.append("Your non-production PID is invalid.")
                return False
            
        if "prod" in self.environments.data:
            if not self.prod_pid.data or self.prod_pid.data.strip() == "":
                # Manually add validation error for prod_pid field
                self.prod_pid.errors.append("You must enter a production PID.")
                return False
            if not (9 <= len(self.prod_pid.data.strip()) <= 11):
                self.prod_pid.errors.append("Your production PID is invalid.")
                return False
            if not self.sc_clearance.data or self.sc_clearance.data != "true":
                # Manually add validation error for sc_clearance field
                self.sc_clearance.errors.append("You must have valid SC Clearance to request access to production environments.")
                return False
            
        return True