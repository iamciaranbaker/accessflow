import bcrypt, base64, os, onetimepass
from accessflow.models.permission import Permission
from accessflow import db, login_manager

class User(db.Model):
    # Table Name
    __tablename__ = "users"

    # Columns
    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    email_address = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(250), nullable = False)
    password_reset_required = db.Column(db.Boolean, nullable = False)
    has_two_factor = db.Column(db.Boolean, default = False, nullable = False)
    two_factor_secret = db.Column(db.String(16))
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Relationships
    permissions = db.relationship("Permission", secondary = "user_permissions", lazy = "joined")

    # Override the default constructor to pass in what we need to create a user.
    # Everything else is set as a default
    def __init__(self, first_name, last_name, email_address, password, password_reset_required):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.set_password(password)
        self.password_reset_required = password_reset_required

    def __repr__(self):
        return f"<User(id = '{self.id}', first_name = '{self.first_name}', last_name = '{self.last_name}', email_address = '{self.email_address}')"

    # Set the password to the hashed value
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Check if password is valid
    def verify_password(self, password):
        try:
            self.password = self.password.encode("utf-8")
        except:
            pass

        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    # Get two factor URI
    def get_two_factor_uri(self):
        return f"otpauth://totp/AccessFlow:{self.email_address}?secret={self.two_factor_secret}&issuer=AccessFlow"

    # Check if two-factor code is valid
    def verify_two_factor(self, code):
        return onetimepass.valid_totp(code, self.two_factor_secret)

    # Generate and set the two-factor base64 secret
    def set_two_factor_secret(self):
        self.two_factor_secret = base64.b32encode(os.urandom(10)).decode("utf-8")

    def has_permission(self, permission_name):
        return any(permission.name == permission_name for permission in self.permissions)
    
    def add_permission(self, permission_name):
        permission = Permission.query.filter(Permission.name == permission_name).first()
        if not permission:
            raise ValueError(f"Permission with name '{permission_name}' does not exist.")
        if permission not in self.permissions:
            self.permissions.append(permission)
            db.session.commit()

    def remove_permission(self, permission_name):
        permission = Permission.query.filter(Permission.name == permission_name).first()
        if not permission:
            raise ValueError(f"Permission with name '{permission_name}' does not exist.")
        if permission in self.permissions:
            self.permissions.remove(permission)
            db.session.commit()

    # Required for flask-login
    def get_id(self):
        return self.id

    # Required for flask-login
    def is_authenticated(self):
        return True

    # Required for flask-login
    def is_active(self):
        return True

    # Required for flask-login
    def is_anonymous(self):
        return False
    
    @staticmethod
    def seed_default():
        if User.query.count() == 0:
            user = User(
                first_name = "Ciaran",
                last_name = "Baker",
                email_address = "ciaran.baker@capgemini.com",
                password = "default",
                password_reset_required = True
            )

            for permission in Permission.get_all():
                user.add_permission(permission.name)

            db.session.add(user)
            db.session.commit()
    
@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()