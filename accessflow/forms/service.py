import re
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, RadioField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, Regexp, EqualTo

class CreateServiceForm(FlaskForm):
    name = StringField("Name", [DataRequired(), Length(min = 2, max = 50), Regexp(regex = r"^([\u00c0-\u01ffa-zA-Z'\-])+$", message = "The entered name is invalid.")])
    project_url = StringField("Project URL", [DataRequired(), Length(min = 2, max = 50)])
    project_access_token = StringField("Project Access Token", [DataRequired(), Length(min = 2, max = 50)])
    force_password_reset = BooleanField("Require password change on first login?")
    submit = SubmitField("Create Service")