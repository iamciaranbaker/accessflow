from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from accessflow.models.team import Team
from accessflow.models.service import Service
import paramiko
import base64

class BaseRequestForm(FlaskForm):
    name = StringField("Name", [
        DataRequired(message = "You must enter a name."),
        Length(min = 2, max = 50, message = "Your name is invalid.")
    ])
    environments = SelectMultipleField("Environments", choices = [
        ("nonprod", "Non-Production"),
        ("prod", "Production")
    ])
    nonprod_pid = StringField("Non-Production PID")
    prod_pid = StringField("Production PID")
    sc_clearance = SelectField(
        "Do you have active SC clearance?",
        choices = [("true", "Yes"), ("false", "No")],
        validate_choice = False
    )
    submit = SubmitField("Create Request")

    def validate_on_submit(self, extra_validators = None):
        if not super().validate_on_submit(extra_validators = extra_validators):
            return False

        if not self.environments.data:
            self.environments.errors.append("You must select at least one environment.")
            return False

        if "nonprod" in self.environments.data:
            if not self.nonprod_pid.data or not self.nonprod_pid.data.strip():
                self.nonprod_pid.errors.append("You must enter a non-production PID.")
                return False
            if not (7 <= len(self.nonprod_pid.data.strip()) <= 9):
                self.nonprod_pid.errors.append("Your non-production PID is invalid.")
                return False

        if "prod" in self.environments.data:
            if not self.prod_pid.data or not self.prod_pid.data.strip():
                self.prod_pid.errors.append("You must enter a production PID.")
                return False
            if not (9 <= len(self.prod_pid.data.strip()) <= 11):
                self.prod_pid.errors.append("Your production PID is invalid.")
                return False
            if not self.sc_clearance.data or self.sc_clearance.data != "true":
                self.sc_clearance.errors.append("You must have valid SC Clearance to request access to production environments.")
                return False

        return True

class AccountCreationRequestForm(BaseRequestForm):
    team = SelectField("Team")
    nonprod_ssh_key = TextAreaField("Non-Production SSH Key")
    prod_ssh_key = TextAreaField("Production SSH Key")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate teams from database
        self.team.choices = [(str(team.id), team.friendly_name) for team in Team.query.all()]

    def validate_on_submit(self, extra_validators = None):
        if not super().validate_on_submit(extra_validators = extra_validators):
            return False
        
        if "nonprod" in self.environments.data:
            if not self.nonprod_ssh_key.data or not self.nonprod_ssh_key.data.strip():
                self.nonprod_ssh_key.errors.append("You must enter a non-production SSH key.")
                return False
            parsed_ssh_key = self.parse_ssh_key(self.nonprod_ssh_key.data)
            if not parsed_ssh_key:
                self.nonprod_ssh_key.errors.append("Your non-production SSH key is invalid.")
                return False
            self.nonprod_ssh_key.data = parsed_ssh_key

        if "prod" in self.environments.data:
            if not self.prod_ssh_key.data or not self.prod_ssh_key.data.strip():
                self.prod_ssh_key.errors.append("You must enter a production SSH key.")
                return False
            parsed_ssh_key = self.parse_ssh_key(self.prod_ssh_key.data)
            if not parsed_ssh_key:
                self.prod_ssh_key.errors.append("Your production SSH key is invalid.")
                return False
            self.prod_ssh_key.data = parsed_ssh_key

        return True

    def parse_ssh_key(self, ssh_key):
        """
        Validates and returns a cleaned SSH key without the comment.
        Returns None if the key is invalid.
        """
        try:
            parts = ssh_key.strip().split()
            if len(parts) < 2:
                return None

            key_type, key_data = parts[0], parts[1]
            key_blob = base64.b64decode(key_data.encode())

            # Validate by attempting to parse it
            if key_type == "ssh-rsa":
                paramiko.RSAKey(data = key_blob)
            elif key_type == "ssh-ed25519":
                paramiko.Ed25519Key(data = key_blob)
            else:
                return None

            # Return normalized key (without comment)
            return f"{key_type} {key_data}"
        except Exception:
            return None

class ServiceAccessRequestForm(BaseRequestForm):
    services = SelectMultipleField("Services")
    justification = TextAreaField("Justification", [DataRequired(message = "You must enter a justification.")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate services from database
        self.services.choices = [(str(service.id), service.name) for service in Service.query.all()]