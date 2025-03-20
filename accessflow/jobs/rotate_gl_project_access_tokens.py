from datetime import timedelta
from accessflow.models.service import Service
from accessflow import db, gitlab_handler

"""
This job iterates through all Services, checks if their GitLab Project Access Tokens are due to expire, and rotates them if Auto Rotation is turned on.
"""
class RotateGLProjectAccessTokens:
    def __init__(self, logger):
        self.logger = logger
        
    def run(self):
        # Return all Services which have an active PAT, have auto rotate turned on, and have PAT's that expire in a day or less
        services = Service.query.filter(
            Service.gl_project_access_token_active == True,
            Service.gl_project_access_token_auto_rotate == True,
            Service.gl_project_access_token_expires_at <= db.session.query(db.func.now()).scalar() + timedelta(days = 1)
        ).all()
        if len(services) == 0:
            self.logger.info("There are no Project Access Tokens to rotate!")
            return
        for service in services:
            token = gitlab_handler.rotate_project_access_token(service.gl_project_access_token)
            if not token or not token["active"] or not token["token"]:
                self.logger.error(f"An error occured whilst rotating the Project Access Token for {service.name}!")
                self.logger.error(f"Project Access Token for {service.name} is no longer valid!")
                service.gl_project_access_token_active = False
                db.session.commit()
                # Something obviously went wrong whilst rotating the PAT, so set the PAT as not active
                break
            # Update the PAT stored in the database
            self.logger.success(f"Project Access Token for {service.name} has been rotated!")
            service.gl_project_access_token = token["token"]
            service.gl_project_access_token_id = token["id"]
            service.gl_project_access_token_expires_at = token["expires_at"]
            db.session.commit()