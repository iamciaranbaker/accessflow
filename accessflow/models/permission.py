from accessflow import db

class Permission(db.Model):
    # Set the DB table name.
    __tablename__ = "permissions"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True, nullable = False)
    name = db.Column(db.String(100), unique = True, nullable = False)
    description = db.Column(db.String(250), nullable = False)