from accessflow import db

class UserPermission(db.Model):
    # Set the DB table name.
    __tablename__ = "user_permissions"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key = True)
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id"), primary_key = True)