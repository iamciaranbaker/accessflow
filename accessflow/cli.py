import click

def register_cli(app):
    from accessflow.models.permission_group import PermissionGroup
    from accessflow.models.permission import Permission
    from accessflow.models.user import User
    from accessflow.models.job import Job
    from accessflow.models.activity_event_type import ActivityEventType
    from accessflow import db

    @app.cli.command("seed-db")
    def seed_database():
        PermissionGroup.seed_all()
        Permission.seed_all()
        User.seed_default()
        Job.seed_all()
        ActivityEventType.seed_all()

    # For use during development ONLY
    @app.cli.command("recreate-db")
    def recreate_database():
        db.drop_all()
        db.session.commit()
        db.create_all()
        db.session.commit()

    @app.cli.command("run-jobs")
    @click.option("--force", is_flag = True, help = "Force run all jobs regardless of if they are due.")
    def run_jobs(force):
        Job.run_all(force = force)