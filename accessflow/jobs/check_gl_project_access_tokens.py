from accessflow.models.service import Service
from accessflow import db, gitlab_handler

"""
This job iterates through all Services and checks their GitLab Project Access Tokens.
If the token has changed (i.e. rotated through the GitLab UI) or revoked, it will get updated in the database.
"""
class CheckGLProjectAccessTokens:
    def __init__(self, logger):
        self.logger = logger
        
    def run(self):
        services = Service.query.filter(Service.gl_project_access_token_active == True).all()
        if len(services) == 0:
            self.logger.info("There are no Project Access Tokens to check!")
            return
        for service in services:
            self.logger.info(f"Checking {service.name}...")
            token = gitlab_handler.get_project_access_token(service.gl_project_access_token)
            if not token or not token["active"]:
                self.logger.error(f"Project Access Token for {service.name} is no longer valid!")
                service.gl_project_access_token_active = False
                db.session.commit()
                # Project Access Token is no longer valid so don't check anything else
                break
            self.logger.success(f"Project Access Token for {service.name} is valid!")
            # The PAT ID might have changed if it was rotated through the GitLab UI
            service.gl_project_access_token_id = token["id"]
            # The PAT expiry date might have changed for the same reason as above
            service.gl_project_access_token_expires_at = token["expires_at"]
            db.session.commit()