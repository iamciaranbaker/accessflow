from accessflow.models.permission_type import PermissionType
from accessflow import db

class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(100), unique = True, nullable = False)
    friendly_name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(250), nullable = False)
    type = db.relationship("PermissionType", backref = db.backref("permissions", lazy = "dynamic"))
    type_id = db.Column(db.Integer, db.ForeignKey("permission_types.id"), nullable = False)
    order_id = db.Column(db.Integer, nullable = False)
    given_by_default = db.Column(db.Boolean, default = False, nullable = False)

def get_all_permissions(ordered = False):
    """
    Retrieve all Permission objects, optionally ordered by PermissionType and Permission order_id.

    Parameters:
      ordered (bool): If True, the permissions are ordered by PermissionType's order_id and then by Permission's order_id. Default is False.

    Returns:
      list: A list of all Permission objects.
    """
    permissions = Permission.query.join(PermissionType, Permission.type_id == PermissionType.id)
    
    if ordered:
        permissions = permissions.order_by(PermissionType.order_id, Permission.order_id)
    
    return permissions.all()