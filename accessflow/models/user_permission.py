from accessflow import db

class UserPermission(db.Model):
    # Table Name
    __tablename__ = "user_permissions"

    # Columns
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key = True)
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id"), primary_key = True)
    assigned_at = db.Column(db.DateTime, default = db.func.now())

    def __repr__(self):
        return f"<UserPermission(user_id = '{self.user_id}', permission_id = '{self.permission_id}')"