from sqlalchemy.dialects.mysql import TIMESTAMP
from accessflow.models.activity_event_type import ActivityEventType
from accessflow import db
import string

class ActivityLogDescriptionFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            parts = key.split(".")
            value = kwargs
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = getattr(value, part, f"<missing: {key}>")
            return value
        return super().get_value(key, args, kwargs)

class ActivityLog(db.Model):
    # Table Name
    __tablename__ = "activity_logs"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    event_type_id = db.Column(db.Integer, db.ForeignKey("activity_event_types.id"), nullable = False)
    target_type = db.Column(db.String(100), nullable = True)
    target_id = db.Column(db.String(50), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "SET NULL"), nullable = True)
    description = db.Column(db.String(255), nullable = True)
    created_at = db.Column(TIMESTAMP(fsp = 6), default = db.func.now(6))

    # Relationships
    event_type = db.relationship("ActivityEventType", backref = "activity_logs")
    user = db.relationship("User", backref = "activity_logs", passive_deletes = True)

    @property
    def target(self):
        if not self.target_type or not self.target_id:
            return None
        
        from accessflow.models.model_registry import model_registry

        model_class = model_registry.get(self.target_type)
        if model_class:
            return db.session.get(model_class, self.target_id)
        return None
    
    @property
    def description(self):
        template = self.event_type.description_template if self.event_type else None
        if not template:
            return None

        formatter = ActivityLogDescriptionFormatter()

        try:
            return formatter.format(
                template,
                user = f"{self.user.first_name} {self.user.last_name}" if self.user else "System",
                target = self.target,
                event_type = self.event_type
            )
        except Exception:
            return None

    def __init__(self, event_type_name, target = None, user_id = None):
        event_type = ActivityEventType.query.filter(ActivityEventType.name == event_type_name).first()
        if not event_type:
            raise ValueError(f"No event type found with name '{event_type_name}'!")
        self.event_type_id = event_type.id
        if target:
            self.target_type = target.__class__.__name__
            self.target_id = getattr(target, "id", None)
            if not self.target_id:
                raise ValueError("Target object must have an 'id' attribute!")
        self.user_id = user_id

    def __repr__(self):
        return f"<ActivityLog(id = '{self.id}', event_type = '{self.event_type.name}')"