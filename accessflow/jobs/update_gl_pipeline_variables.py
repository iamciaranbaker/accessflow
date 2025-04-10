from accessflow.models.service import Service
from accessflow import gitlab_handler
import json

class UpdateGLPipelineVariables:
    def __init__(self, logger, session):
        self.logger = logger
        self.session = session
        
    def run(self):
        services = self.session.query(Service).filter(Service.gl_project_access_token_active == True).all()
        if len(services) == 0:
            self.logger.info("There are no services available!")
            return
        for service in services:
            self.logger.info(f"Updating pipeline variables for {service.name}...")
            service.gl_pipeline_variables = json.dumps(gitlab_handler.get_project_pipeline_variables(service.gl_project_url, service.gl_project_access_token))
            self.session.commit()