import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp, EqualTo
from access_flow.models.user import User

"""
Passwords need to:
  * be at least 8 characters long
  * contain at least one lowercase letter
  * contain at least one uppercase letter
  * contain at least one digit
  * contain at least one symbol
"""

def password_validator(form, field):
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
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")

class TwoFactorForm(FlaskForm):
    code = StringField("Two-Factor Code", [DataRequired(), Length(min = 6, max = 6)])
    submit = SubmitField("Login")

class UpdatePasswordForm(FlaskForm):
    password = PasswordField("Password", [DataRequired(), password_validator])
    confirm_password = PasswordField("Confirm Password", [DataRequired(), EqualTo("password", message = "The entered passwords must match.")])
    submit = SubmitField("Update Password")