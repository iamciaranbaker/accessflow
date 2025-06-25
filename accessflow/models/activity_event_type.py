from accessflow import logger, db

class ActivityEventType(db.Model):
    # Table Name
    __tablename__ = "activity_event_types"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    friendly_name = db.Column(db.String(100), nullable = False)
    description_template = db.Column(db.String(255), nullable = True)
    badge_icon = db.Column(db.String(30), nullable = True)
    badge_color = db.Column(db.String(10), nullable = True)
    show_in_sentinel = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    def __init__(self, name, friendly_name, description_template = None, badge_icon = None, badge_color = None, show_in_sentinel = True):
        self.name = name
        self.friendly_name = friendly_name
        self.description_template = description_template
        self.badge_icon = badge_icon
        self.badge_color = badge_color
        self.show_in_sentinel = show_in_sentinel

    def __repr__(self):
        return f"<ActivityEventType(id = '{self.id}', name = '{self.name}', friendly_name = '{self.friendly_name}', description_template = '{self.description_template}')"

    @staticmethod
    def seed_all():
        activity_event_types = [
            ActivityEventType(
                name = "login",
                friendly_name = "Login",
                show_in_sentinel = False
            ),
            ActivityEventType(
                name = "logout",
                friendly_name = "Logout",
                show_in_sentinel = False
            ),
            ActivityEventType(
                name = "login_attempt",
                friendly_name = "Login Attempt",
                show_in_sentinel = False
            ),
            ActivityEventType(
                name = "service_create",
                friendly_name = "Service Created",
                description_template = "<b>{user}</b> created service <b>{target.name}</b>",
                badge_icon = "fa-server",
                badge_color = "success"
            ),
            ActivityEventType(
                name = "service_delete",
                friendly_name = "Service Deleted",
                description_template = "<b>{user}</b> deleted service <b>{target.name}</b>",
                badge_icon = "fa-server",
                badge_color = "danger"
            ),
            ActivityEventType(
                name = "job_trigger",
                friendly_name = "Job Triggered",
                description_template = '<b>{user}</b> triggered job <b>{target.job.name}</b>',
                badge_icon = "fa-wrench",
                badge_color = "secondary"
            )
        ]

        for activity_event_type in activity_event_types:
            existing_activity_event_type = ActivityEventType.query.filter(ActivityEventType.name == activity_event_type.name).first()
            if existing_activity_event_type:
                existing_activity_event_type.friendly_name = activity_event_type.friendly_name
                existing_activity_event_type.description_template = activity_event_type.description_template
                existing_activity_event_type.badge_icon = activity_event_type.badge_icon
                existing_activity_event_type.badge_color = activity_event_type.badge_color
                logger.info(f"Updating {existing_activity_event_type}")
            else:
                db.session.add(activity_event_type)
                logger.info(f"Creating {activity_event_type}")

        db.session.commit()