from accessflow import logger, db

class ActivityEventType(db.Model):
    # Table Name
    __tablename__ = "activity_event_types"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    friendly_name = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    def __init__(self, name, friendly_name):
        self.name = name
        self.friendly_name = friendly_name

    def __repr__(self):
        return f"<ActivityEventType(id = '{self.id}', name = '{self.name}', friendly_name = '{self.friendly_name}')"

    @staticmethod
    def seed_all():
        activity_event_types = [
            ActivityEventType("login", "Login"),
            ActivityEventType("logout", "Logout"),
            ActivityEventType("login_attempt", "Login Attempt"),
            ActivityEventType("service_create", "Service Created"),
            ActivityEventType("service_delete", "Service Deleted")
        ]

        for activity_event_type in activity_event_types:
            existing_activity_event_type = ActivityEventType.query.filter(ActivityEventType.name == activity_event_type.name).first()
            if existing_activity_event_type:
                existing_activity_event_type.friendly_name = activity_event_type.friendly_name
                logger.info(f"Updating {existing_activity_event_type}")
            else:
                db.session.add(activity_event_type)
                logger.info(f"Creating {activity_event_type}")

        db.session.commit()