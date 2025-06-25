from sqlalchemy.dialects.mysql import JSON, TIMESTAMP
from accessflow.models.activity_event_type import ActivityEventType
from accessflow.models.user import User
from accessflow import db
import string

class ActivityLogDescriptionFormatter(string.Formatter):
    def get_field(self, field_name, args, kwargs):
        parts = field_name.split(".")
        obj = kwargs.get(parts[0])

        for part in parts[1:]:
            if isinstance(obj, dict):
                obj = obj.get(part)
            else:
                obj = getattr(obj, part, None)

            if obj is None:
                break

        return obj, field_name

class ActivityLog(db.Model):
    # Table Name
    __tablename__ = "activity_logs"

    # Columns
    id = db.Column(db.Integer, primary_key = True)
    event_type_id = db.Column(db.Integer, db.ForeignKey("activity_event_types.id"), nullable = False)
    target_id = db.Column(db.Integer, nullable = True)
    target_type = db.Column(db.String(100), nullable = True)
    target_metadata = db.Column(JSON, nullable = True)
    user_id = db.Column(db.Integer, nullable = True) # Not a foreign key to preserve user ID on deletion
    user_metadata = db.Column(JSON, nullable = True)
    created_at = db.Column(TIMESTAMP(fsp = 6), default = db.func.now(6))

    # Relationships
    event_type = db.relationship("ActivityEventType", lazy = "select")

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
    def user(self):
        if not self.user_id:
            return None
        
        return db.session.get(User, self.user_id)
    
    @property
    def description(self):
        template = self.event_type.description_template if self.event_type else None
        if not template:
            return None

        formatter = ActivityLogDescriptionFormatter()

        if self.user:
            user_value = f"{self.user.first_name} {self.user.last_name}"
        elif self.user_metadata:
            first = self.user_metadata.get("first_name", "")
            last = self.user_metadata.get("last_name", "")
            user_value = f"{first} {last}".strip() or "System"
        else:
            user_value = "System"

        try:
            return formatter.format(
                template,
                user = user_value,
                target = self.target or self.target_metadata or {},
                event_type = self.event_type
            )
        except Exception:
            return None

    def __init__(self, event_type_name, target = None, user = None):
        event_type = ActivityEventType.query.filter(ActivityEventType.name == event_type_name).first()
        if not event_type:
            raise ValueError(f"No event type found with name '{event_type_name}'!")
        self.event_type_id = event_type.id
        if target:
            self.target_id = getattr(target, "id", None)
            self.target_type = target.__class__.__name__
            self.target_metadata = self.extract_metadata(target)
        if user:
            self.user_id = getattr(user, "id", None)
            self.user_metadata = self.extract_metadata(user)

    def __repr__(self):
        return f"<ActivityLog(id = '{self.id}', event_type = '{self.event_type.name}')"
    
    def extract_metadata(self, target):
        fields = [
            "name",
            "friendly_name",
            "first_name", # For User model
            "last_name" # For User model
        ]
        metadata = {}

        for field in fields:
            value = getattr(target, field, None)
            if value is not None:
                metadata[field] = value

        return metadata