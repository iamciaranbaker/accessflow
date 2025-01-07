import bcrypt, base64, os, onetimepass
from datetime import datetime
from accessflow.utils import get_permission_by_name
from accessflow import db

class User(db.Model):
    # Set the DB table name.
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    email_address = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(250), nullable = False)
    has_two_factor = db.Column(db.Boolean, default = False, nullable = False)
    two_factor_secret = db.Column(db.String(16), nullable = False)
    permissions = db.relationship("Permission", secondary = "user_permissions", backref = db.backref("users", lazy = "dynamic"))
    created_at = db.Column(db.DateTime, nullable = False)

    # Override the default constructor to pass in what we need to create a user. Everything else is set as a default.
    def __init__(self, first_name, last_name, email_address):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.created_at = datetime.now()

    # Set the password to the hashed value.
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Check if password is valid.
    def verify_password(self, password):
        try:
            self.password = self.password.encode("utf-8")
        except:
            pass

        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    # Get two factor URI.
    def get_two_factor_uri(self):
        return f"otpauth://totp/AccessFlow:{self.email_address}?secret={self.two_factor_secret}&issuer=AccessFlow"

    # Check if two-factor code is valid.
    def verify_two_factor(self, code):
        return onetimepass.valid_totp(code, self.two_factor_secret)

    # Reset the two-factor base64 secret.
    def reset_two_factor(self):
        self.two_factor_secret = base64.b32encode(os.urandom(10)).decode("utf-8")

    def has_permission(self, name):
        return any(permission.name == name for permission in self.permissions)
    
    def add_permission(self, name):
        permission = get_permission_by_name(name)
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, name):
        permission = get_permission_by_name(name)
        if permission in self.permissions:
            self.permissions.remove(permission)

    # Required for flask-login.
    def get_id(self):
        return self.id

    # Required for flask-login.
    def is_authenticated(self):
        return True

    # Required for flask-login.
    def is_active(self):
        return True

    # Required for flask-login.
    def is_anonymous(self):
        return False

def get_all_users():
    """
    Retrieve all User objects.

    Returns:
      list: A list of all User objects.
    """
    return User.query.all()