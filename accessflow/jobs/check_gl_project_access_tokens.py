from accessflow.models.service import Service
from accessflow import db

class CheckGLProjectAccessTokens:
    def run(self):
        services = Service.get_all()