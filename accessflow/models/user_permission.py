from accessflow import db

class UserPermission(db.Model):
    # Table Name
    __tablename__ = "user_permissions"

    # Columns
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key = True)
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id"), primary_key = True)
    assigned_at = db.Column(db.DateTime, default = db.func.now())