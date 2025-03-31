from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, TextAreaField, SubmitField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired, Length, Regexp
from accessflow.models.service import Service
from accessflow.config import Config
from accessflow import gitlab_handler

class CreateRequestForm(FlaskForm):
    name = StringField("Name", [DataRequired(), Length(min = 2, max = 50), Regexp(regex = r"/^[a-z ,.'-]+$/i", message = "Name is invalid.")])
    services = SelectMultipleField("Services")
    environments = SelectMultipleField("Environments", choices = [("nonprod", "Non-Production"), ("prod", "Production")])
    nonprod_pid = StringField("Non-Production PID", [Length(min = 7, max = 9)]) # Accomodate CG and U. - e.g. cg19321, u.8904064
    prod_pid = StringField("Production PID", [Length(min = 9, max = 11)]) # Accomodate U. and LSS. - e.g. u.8904064, LSS.8904064
    sc_clearance = SelectField("Do you have active SC clearance?", choices = [("yes", "Yes"), ("no", "No")])
    justification = TextAreaField("Justification", [DataRequired()])
    submit = SubmitField("Create Request")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.services.choices = [(str(service.id), service.name) for service in Service.query.all()]