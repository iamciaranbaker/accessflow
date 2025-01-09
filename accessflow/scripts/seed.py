from accessflow.models.permission_group import PermissionGroup
from accessflow.models.permission import Permission
from accessflow.models.user import User
from accessflow import app

@app.cli.command("seed-db")
def seed_database():
    PermissionGroup.seed_all()
    Permission.seed_all()
    User.seed_default()