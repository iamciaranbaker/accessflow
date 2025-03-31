from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, RadioField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, Regexp, EqualTo
from accessflow.models.user import User
from accessflow.models.permission import Permission
import re

def email_address_validator(form, field):
    # Check if user already exists with given email address
    user = User.query.filter(User.email_address == field.data).first()
    if user:
        raise ValidationError("Email address is already in use.")

def password_validator(form, field):
    """
    Passwords need to:
    * be at least 8 characters long
    * contain at least one lowercase letter
    * contain at least one uppercase letter
    * contain at least one digit
    * contain at least one symbol
    """

    # Define error cases
    length_error = len(field.data) < 8
    lowercase_error = re.search(r"[a-z]", field.data) is None
    uppercase_error = re.search(r"[A-Z]", field.data) is None
    digit_error = re.search(r"\d", field.data) is None
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', field.data) is None

    # Check if any error cases have been matched
    if length_error:
        raise ValidationError("Password must be at least 8 characters.")
    elif lowercase_error:
        raise ValidationError("Password must contain a lowercase letter.")
    elif uppercase_error:
        raise ValidationError("Password must contain an uppercase letter.")
    elif digit_error:
        raise ValidationError("Password must contain a number.")
    elif symbol_error:
        raise ValidationError("Password must contain a symbol.")

class LoginForm(FlaskForm):
    email_address = EmailField("Email Address", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")

class TwoFactorForm(FlaskForm):
    code = StringField("Two-Factor Code", [DataRequired(), Length(min = 6, max = 6)])
    submit = SubmitField("Login")

class UpdatePasswordForm(FlaskForm):
    password = PasswordField("Password", [DataRequired(), password_validator])
    confirm_password = PasswordField("Confirm Password", [DataRequired(), EqualTo("password", message = "Both passwords must match.")])
    submit = SubmitField("Update Password")

class CreateUserForm(FlaskForm):
    first_name = StringField("First Name", [DataRequired(), Length(min = 2, max = 50), Regexp(regex = r"^([\u00c0-\u01ffa-zA-Z'\-])+$", message = "First name is invalid.")])
    last_name = StringField("Last Name", [DataRequired(), Length(min = 2, max = 50), Regexp(regex = r"^([\u00c0-\u01ffa-zA-Z'\-])+$", message = "Last name is invalid.")])
    email_address = EmailField("Email Address", [DataRequired(), Length(max = 100), Email(message = "The entered email address is invalid."), email_address_validator])
    password = PasswordField("Password", [DataRequired(), password_validator])
    confirm_password = PasswordField("Confirm Password", [DataRequired(), EqualTo("password", message = "Both passwords must match.")])
    force_password_reset = BooleanField("Require password change on first login?")
    submit = SubmitField("Create User")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_groups = []
        self.populate_permissions()

    def populate_permissions(self):
        # Retrieve all permissions ordered by their group's display order and then by permission's display order
        permissions = Permission.get_all(ordered = True)

        current_permission_group = None # Track the current permission group dictionary

        for permission in permissions:
            # Check if the permission belongs to a new group
            if not current_permission_group or current_permission_group["permission_group"] != permission.group:
                # Append the completed group to the permissions list
                if current_permission_group:
                    self.permission_groups.append(current_permission_group)

                # Start a new permission group
                current_permission_group = {
                    "permission_group": permission.group, # The PermissionGroup object
                    "permissions": [] # Initialize a new list for this group's permissions
                }

            # Dynamically create and bind RadioField for the current permission
            field = RadioField(
                choices = [("true", "Yes"), ("false", "No")],
                default = "true" if permission.given_by_default else "false",
            )
            field_name = f"permission[{permission.name}]"

            # Bind the field to the form and set its default value
            bound_field = field.bind(self, field_name)
            bound_field.data = bound_field.default

            # Add the field to the form
            setattr(self, field_name, bound_field)

            # Add the permission and its field to the current permission group
            current_permission_group["permissions"].append({
                "permission": permission,
                "field": bound_field
            })

        # Append the last permission group to the permissions object, if it has permissions
        if current_permission_group:
            self.permission_groups.append(current_permission_group)