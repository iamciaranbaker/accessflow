from flask_sqlalchemy import SQLAlchemy
from accessflow import db

class PermissionGroup(db.Model):
    # Table Name
    __tablename__ = "permission_groups"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    friendly_name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(255))
    display_order = db.Column(db.Integer, default = 1)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    def __init__(self, name, friendly_name, description = None, display_order = 1):
        self.name = name
        self.friendly_name = friendly_name
        self.description = description
        self.display_order = display_order

    def __repr__(self):
        return f"<PermissionGroup(id=\"{self.id}\", name=\"{self.name}\")"

    @staticmethod
    def seed_all():
        permission_groups = [
            PermissionGroup("general", "General", display_order = 1),
            PermissionGroup("admin", "Administrator", display_order = 2)
        ]

        for permission_group in permission_groups:
            existing_permission_group = PermissionGroup.query.filter_by(name = permission_group.name).first()
            if existing_permission_group:
                existing_permission_group.friendly_name = permission_group.friendly_name
                existing_permission_group.description = permission_group.description
                existing_permission_group.display_order = permission_group.display_order
                print(f"Updated {existing_permission_group}")
            else:
                db.session.add(permission_group)
                print(f"Created {permission_group}")

        db.session.commit()