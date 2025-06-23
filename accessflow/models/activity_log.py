from sqlalchemy.dialects.mysql import TIMESTAMP
from accessflow.models.activity_event_type import ActivityEventType
from accessflow import db

class ActivityLog(db.Model):
    # Table Name
    __tablename__ = "activity_logs"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    event_type_id = db.Column(db.Integer, db.ForeignKey("activity_event_types.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "SET NULL"), nullable = True)
    user_name = db.Column(db.String(150), nullable = True)
    created_at = db.Column(TIMESTAMP(fsp = 6), default = db.func.now(6))

    # Relationships
    user = db.relationship("User", backref = "activity_logs", passive_deletes = True)
    event_type = db.relationship("ActivityEventType", backref = "activity_logs")

    def __init__(self, event_type_name, user = None):
        event_type = ActivityEventType.query.filter(ActivityEventType.name == event_type_name).first()
        if not event_type:
            raise ValueError(f"No event type found with name '{event_type_name}'!")
        self.event_type_id = event_type.id
        self.user_id = user.id
        self.user_name = f"{user.first_name} {user.last_name}" or None

    def __repr__(self):
        return f"<ActivityLog(id = '{self.id}', event_type = '{self.event_type.name}')"