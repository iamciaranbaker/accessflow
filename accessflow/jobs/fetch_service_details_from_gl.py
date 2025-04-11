from accessflow.models.service import Service
from accessflow.models.service_environment import ServiceEnvironment, ServiceEnvironmentType
from accessflow.models.service_host_group import ServiceHostGroup

class FetchServiceDetailsFromGL:
    def __init__(self, logger, session):
        self.logger = logger
        self.session = session

    def run(self, service_id):
        # Fetch service object from database
        service = self.session.query(Service).filter(Service.id == service_id).first()
        # Ensure service exists.
        # It should, as it's either just been created, or being updated periodically to ensure it's up-to-date
        if not service:
            self.logger.error(f"Could not find service with ID '{service_id}'!")
            raise Exception
        
        self.logger.info(f"Deleting existing environments and host groups for {service.name}...")

        # Delete existing service environments and host groups
        self.session.query(ServiceEnvironment).filter(ServiceEnvironment.service_id == service_id).delete()
        self.session.query(ServiceHostGroup).filter(ServiceHostGroup.service_id == service_id).delete()

        # Fetch the latest pipeline variables from the project
        pipeline_variables = service.get_pipeline_variables()

        # Iterate through the ENV_TYPE options
        for i, environment in enumerate(pipeline_variables["ENV_TYPE"]["options"]):
            service_environment = ServiceEnvironment(
                service_id = service_id,
                name = environment,
                type = self.calculate_environment_type(environment),
                order = i + 1
            )
            self.session.add(service_environment)
            self.logger.info(f"Creating {service_environment}")
        # Iterate through the HOST_GROUP options
        for i, host_group in enumerate(pipeline_variables["HOST_GROUP"]["options"]):
            service_host_group = ServiceHostGroup(
                service_id = service_id,
                name = host_group,
                order = i + 1
            )
            self.session.add(service_host_group)
            self.logger.info(f"Creating {service_host_group}")

        # Commit changes to database
        self.session.commit()

    def calculate_environment_type(self, name):
        name = name.lower()

        if any(keyword in name for keyword in ["test", "dev", "fst", "ist", "isit", "sit", "ci", "nonprod", "nonproduction", "non-prod", "non-production"]):
            return ServiceEnvironmentType.NONPROD
        elif any(keyword in name for keyword in ["preprod", "pre-prod", "prod"]):
            return ServiceEnvironmentType.PROD
        else:
            return ServiceEnvironmentType.UNKNOWN