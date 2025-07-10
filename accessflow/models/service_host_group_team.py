from accessflow import db

class ServiceHostGroupTeam(db.Model):
    # Table Name
    __tablename__ = "service_host_group_teams"

    # Columns
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), primary_key = True)
    name = db.Column(db.String(30), primary_key = True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), primary_key = True)

    def __init__(self, service_id, name, team_id):
        self.service_id = service_id
        self.name = name
        self.team_id = team_id

    def __repr__(self):
        return f"<ServiceHostGroupTeam(service_id = '{self.service_id}', name = '{self.name}', team_id = '{self.team_id}')"