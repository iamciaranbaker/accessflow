from accessflow.models.user import User
from accessflow.models.permission_type import PermissionType
from accessflow.models.permission import Permission
from accessflow.utils import get_all_permissions, get_permission_type_by_name
from accessflow import app, db

def seed_permission_types():
    permission_types = [
        {
            "name": "requests",
            "friendly_name": "Requests",
            "description": "",
            "order_id": 1
        },
        {
            "name": "users",
            "friendly_name": "Users",
            "description": "",
            "order_id": 2
        },
        {
            "name": "groups",
            "friendly_name": "Groups",
            "description": "",
            "order_id": 3
        },
        {
            "name": "services",
            "friendly_name": "Services",
            "description": "",
            "order_id": 4
        },
        {
            "name": "admin",
            "friendly_name": "Administration",
            "description": "",
            "order_id": 5
        }
    ]

    for permission_type_data in permission_types:
        # Check if the permission type already exists.
        permission_type = PermissionType.query.filter_by(name = permission_type_data["name"]).first()
        
        if permission_type:
            # Update the permission type if any attributes have changed.
            updated = False

            if permission_type.friendly_name != permission_type_data["friendly_name"]:
                permission_type.friendly_name = permission_type_data["friendly_name"]
                updated = True

            if permission_type.description != permission_type_data["description"]:
                permission_type.description = permission_type_data["description"]
                updated = True

            if permission_type.order_id != permission_type_data["order_id"]:
                permission_type.order_id = permission_type_data["order_id"]
                updated = True

            if updated:
                print(f"Updated existing permission type: {permission_type.name}")
        else:
            # Add a new permission type if it doesn't exist.
            permission_type = PermissionType(
                name = permission_type_data["name"],
                friendly_name = permission_type_data["friendly_name"],
                description = permission_type_data["description"],
                order_id = permission_type_data["order_id"]
            )
            db.session.add(permission_type)
            print(f"Added new permission type: {permission_type.name}")

    # Commit all changes to the database.
    db.session.commit()

def seed_permissions():
    permissions = [
        {
            "name": "view_requests",
            "friendly_name": "View Requests",
            "description": "",
            "type": "requests",
            "order_id": 1
        },
        {
            "name": "view_users",
            "friendly_name": "View Users",
            "description": "",
            "type": "users",
            "order_id": 2
        },
        {
            "name": "edit_user",
            "friendly_name": "Edit Users",
            "description": "",
            "type": "users",
            "order_id": 3
        },
        {
            "name": "delete_user",
            "friendly_name": "Delete Users",
            "description": "",
            "type": "users",
            "order_id": 4
        },
        {
            "name": "view_groups",
            "friendly_name": "View Groups",
            "description": "",
            "type": "groups",
            "order_id": 5
        },
        {
            "name": "edit_groups",
            "friendly_name": "Edit Groups",
            "description": "",
            "type": "groups",
            "order_id": 6
        },
        {
            "name": "delete_groups",
            "friendly_name": "Delete Groups",
            "description": "",
            "type": "groups",
            "order_id": 7
        },
        {
            "name": "view_services",
            "friendly_name": "View Services",
            "description": "",
            "type": "services",
            "order_id": 8
        },
        {
            "name": "edit_services",
            "friendly_name": "Edit Services",
            "description": "",
            "type": "services",
            "order_id": 9
        },
        {
            "name": "delete_services",
            "friendly_name": "Delete Services",
            "description": "",
            "type": "services",
            "order_id": 10
        },
        {
            "name": "view_users",
            "friendly_name": "View Users",
            "description": "",
            "type": "admin",
            "order_id": 11
        },
        {
            "name": "edit_users",
            "friendly_name": "Edit Users",
            "description": "",
            "type": "admin",
            "order_id": 12
        },
        {
            "name": "delete_users",
            "friendly_name": "Delete Users",
            "description": "",
            "type": "admin",
            "order_id": 13
        }
    ]

    for permission_data in permissions:
        # Check if the permission already exists.
        permission = Permission.query.filter_by(name = permission_data["name"]).first()
        
        if permission:
            # Update the permission if any attributes have changed.
            updated = False

            if permission.friendly_name != permission_data["friendly_name"]:
                permission.friendly_name = permission_data["friendly_name"]
                updated = True

            if permission.description != permission_data["description"]:
                permission.description = permission_data["description"]
                updated = True
            
            if permission.type_id != get_permission_type_by_name(permission_data["type"]).id:
                permission.type_id = get_permission_type_by_name(permission_data["type"]).id
                updated = True

            if permission.order_id != permission_data["order_id"]:
                permission.order_id = permission_data["order_id"]
                updated = True

            if updated:
                print(f"Updated existing permission: {permission.name}")
        else:
            # Add a new permission if it doesn't exist.
            permission = Permission(
                name = permission_data["name"],
                friendly_name = permission_data["friendly_name"],
                description = permission_data["description"],
                type_id = get_permission_type_by_name(permission_data["type"]).id,
                order_id = permission_data["order_id"]
            )
            db.session.add(permission)
            print(f"Added new permission: {permission.name}")

    # Commit all changes to the database.
    db.session.commit()

def seed_default_user():
    if User.query.count() == 0:
        user = User(
            first_name = "Default",
            last_name = "Default",
            email_address = "default@example.com"
        )
        user.set_password("default")
        user.reset_two_factor()

        for permission in get_all_permissions():
            user.add_permission(permission.name)

        db.session.add(user)
        db.session.commit()

@app.cli.command("seed-db")
def seed_database():
    seed_permission_types()
    seed_permissions()
    seed_default_user()
    print("Database seeded successfully.")