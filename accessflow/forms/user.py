import re
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, RadioField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, Regexp, EqualTo
from accessflow.models.user import User
from accessflow.models.permission import get_all_permissions

def email_address_validator(form, field):
    # Check if user already exists with given email address.
    user = User.query.filter_by(email_address = field.data).first()
    if user:
        raise ValidationError("Your email address is already in use.")

def password_validator(form, field):
    """
    Passwords need to:
    * be at least 8 characters long
    * contain at least one lowercase letter
    * contain at least one uppercase letter
    * contain at least one digit
    * contain at least one symbol
    """

    # Define error cases.
    length_error = len(field.data) < 8
    lowercase_error = re.search(r"[a-z]", field.data) is None
    uppercase_error = re.search(r"[A-Z]", field.data) is None
    digit_error = re.search(r"\d", field.data) is None
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', field.data) is None

    # Check if any error cases have been matched.
    if length_error:
        raise ValidationError("Your password must be at least 8 characters.")
    elif lowercase_error:
        raise ValidationError("Your password must contain a lowercase letter.")
    elif uppercase_error:
        raise ValidationError("Your password must contain an uppercase letter.")
    elif digit_error:
        raise ValidationError("Your password must contain a number.")
    elif symbol_error:
        raise ValidationError("Your password must contain a symbol.")

class LoginForm(FlaskForm):
    email_address = EmailField("Email Address", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")

class TwoFactorForm(FlaskForm):
    code = StringField("Two-Factor Code", [DataRequired(), Length(min = 6, max = 6)])
    submit = SubmitField("Login")

class UpdatePasswordForm(FlaskForm):
    password = PasswordField("Password", [DataRequired(), password_validator])
    confirm_password = PasswordField("Confirm Password", [DataRequired(), EqualTo("password", message = "The entered passwords must match.")])
    submit = SubmitField("Update Password")

class CreateUserForm(FlaskForm):
    first_name = StringField("First Name", [DataRequired(), Length(min = 2, max = 50), Regexp(regex = r"^([\u00c0-\u01ffa-zA-Z'\-])+$", message = "The entered first name is invalid.")])
    last_name = StringField("Last Name", [DataRequired(), Length(min = 2, max = 50), Regexp(regex = r"^([\u00c0-\u01ffa-zA-Z'\-])+$", message = "The entered last name is invalid.")])
    email_address = EmailField("Email Address", [DataRequired(), Length(max = 100), Email(message = "The entered email address is invalid."), email_address_validator])
    password = PasswordField("Password", [DataRequired(), password_validator])
    confirm_password = PasswordField("Confirm Password", [DataRequired(), EqualTo("password", message = "The entered passwords must match.")])
    force_password_reset = BooleanField("Require password change on first login?")
    submit = SubmitField("Create User")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_groups = []
        self.populate_permissions()

    def populate_permissions(self):
        permissions = get_all_permissions(ordered = True)

        current_type_id = None
        current_group = {"permission_type": None, "permission_fields": []}

        for permission in permissions:
            if permission.type_id != current_type_id:
                if current_group["permission_fields"]:
                    self.permission_groups.append(current_group)

                current_group = {"permission_type": permission.type, "permission_fields": []}
                current_type_id = permission.type_id

            # Dynamically create and bind the field.
            field = RadioField(
                label = permission.friendly_name,
                choices = [("true", "Yes"), ("false", "No")],
                default = "true" if permission.given_by_default else "false",
                description = permission.description
            )
            field_name = f"permission[{permission.name}]"

            # Bind the field to the form and set its default value to its data attribute.
            bound_field = field.bind(self, field_name)
            bound_field.data = bound_field.default

            setattr(self, field_name, bound_field)

            current_group["permission_fields"].append(bound_field)

        if current_group["permission_fields"]:
            self.permission_groups.append(current_group)