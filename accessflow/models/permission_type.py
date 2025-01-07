from accessflow import db

class PermissionType(db.Model):
    __tablename__ = "permission_types"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(100), unique = True, nullable = False)
    friendly_name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(250), nullable = False)
    order_id = db.Column(db.Integer, nullable = False)