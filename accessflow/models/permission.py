from accessflow.models.permission_group import PermissionGroup
from accessflow import logger, db

class Permission(db.Model):
    # Table Name
    __tablename__ = "permissions"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    friendly_name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(255))
    group_id = db.Column(db.Integer, db.ForeignKey("permission_groups.id"), nullable = False)
    display_order = db.Column(db.Integer, default = 1)
    given_by_default = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    # Relationships
    group = db.relationship("PermissionGroup", lazy = "joined")

    def __init__(self, name, friendly_name, group_id, description = None, display_order = 1, given_by_default = False):
        self.name = name
        self.friendly_name = friendly_name
        self.group_id = group_id
        self.description = description
        self.display_order = display_order
        self.given_by_default = given_by_default

    def __repr__(self):
        return f"<Permission(id = '{self.id}', name = '{self.name}', friendly_name = '{self.friendly_name}', group_id = '{self.group_id}')"
    
    @staticmethod
    def seed_all():
        permissions = [
            Permission("list_requests", "List Requests", 1, description = "The ability to list requests.", display_order = 1, given_by_default = True),
            Permission("list_users", "List Users", 2, description = "The ability to list users.", display_order = 2),
            Permission("create_users", "Create Users", 2, description = "The ability to create users.", display_order = 3),
            Permission("edit_users", "Edit Users", 2, description = "The ability to edit users.", display_order = 4),
            Permission("delete_users", "Delete Users", 2, description = "The ability to delete users.", display_order = 5),
            Permission("list_services", "List Services", 2, description = "The ability to list services.", display_order = 6),
            Permission("create_services", "Create Services", 2, description = "The ability to create services.", display_order = 7),
            Permission("edit_services", "Edit Services", 2, description = "The ability to edit services.", display_order = 8),
            Permission("delete_services", "Delete Services", 2, description = "The ability to delete services.", display_order = 9),
            Permission("list_jobs", "List Jobs", 2, description = "The ability to list jobs.", display_order = 10),
            Permission("run_jobs", "Run Jobs", 2, description = "The ability to run jobs.", display_order = 11)
        ]

        for permission in permissions:
            existing_permission = Permission.query.filter(Permission.name == permission.name).first()
            if existing_permission:
                existing_permission.friendly_name = permission.friendly_name
                existing_permission.description = permission.description
                existing_permission.display_order = permission.display_order
                logger.info(f"Updating {existing_permission}")
            else:
                db.session.add(permission)
                logger.info(f"Creating {permission}")

        db.session.commit()

    @staticmethod
    def get_all(ordered = False):
        permissions = Permission.query.join(PermissionGroup, Permission.group_id == PermissionGroup.id)
    
        if ordered:
            permissions = permissions.order_by(PermissionGroup.display_order, Permission.display_order)
        
        return permissions.all()