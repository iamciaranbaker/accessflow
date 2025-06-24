from accessflow import logger, db

class ActivityEventType(db.Model):
    # Table Name
    __tablename__ = "activity_event_types"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    description_template = db.Column(db.String(255), nullable = True)
    fa_icon = db.Column(db.String(30), nullable = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())

    def __init__(self, name, description_template = None, fa_icon = None):
        self.name = name
        self.description_template = description_template
        self.fa_icon = fa_icon

    def __repr__(self):
        return f"<ActivityEventType(id = '{self.id}', name = '{self.name}', description_template = '{self.description_template}')"

    @staticmethod
    def seed_all():
        activity_event_types = [
            ActivityEventType("login"),
            ActivityEventType("logout"),
            ActivityEventType("login_attempt"),
            ActivityEventType("service_create", "{user} created service {target.name}", "fa-server"),
            ActivityEventType("service_delete", "{user} deleted service {target.name}", "fa-server"),
            ActivityEventType("job_trigger", "{user} triggered job #{target.id}", "fa-wrench")
        ]

        for activity_event_type in activity_event_types:
            existing_activity_event_type = ActivityEventType.query.filter(ActivityEventType.name == activity_event_type.name).first()
            if existing_activity_event_type:
                existing_activity_event_type.description_template = activity_event_type.description_template
                logger.info(f"Updating {existing_activity_event_type}")
            else:
                db.session.add(activity_event_type)
                logger.info(f"Creating {activity_event_type}")

        db.session.commit()