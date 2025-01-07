from accessflow.models.user import User
from accessflow.models.permission import Permission
from accessflow import app, db

def seed_default_user():
    if User.query.count() == 0:
        user = User(
            first_name = "Default",
            last_name = "Default",
            email_address = "default@example.com"
        )
        user.set_password("default")
        user.reset_two_factor()
        db.session.add(user)
        db.session.commit()

def seed_permissions():
    permissions = [
        {"name": "view_user", "description": "Example description for view_user"},
        {"name": "edit_user", "description": "Example description for edit_user"}
    ]

    for permission in permissions:
        if not Permission.query.filter_by(name = permission["name"]).first():
            permission = Permission(
                name = permission["name"],
                description = permission["description"]
            )
            db.session.add(permission)

    db.session.commit()

@app.cli.command("seed-db")
def seed_database():
    seed_default_user()
    seed_permissions()
    print("Database seeded successfully.")