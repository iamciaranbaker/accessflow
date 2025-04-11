from accessflow.models.team import Team
from accessflow.models.pid import PID, PIDEnvironmentType
from accessflow.config import Config
from accessflow import gitlab_handler
import yaml

class FetchPIDsFromGL:
    def __init__(self, logger, session):
        self.logger = logger
        self.session = session

    def run(self):
        # Get teams and PIDs from database
        teams = self.session.query(Team).all()
        pids = self.session.query(PID).all()
        # Keep track of all PIDs from GitLab and map them to their respective name, comment and team ID
        pids_from_gl = {}

        # Create empty dictionaries within the pids from GL map
        for environment_type in PIDEnvironmentType:
            pids_from_gl[environment_type] = {}

        for team in teams:
            for environment_type in PIDEnvironmentType:
                environment_file = gitlab_handler.get_project_repository_file(Config.SUPPORT_USERS_PROJECT_URL, Config.SUPPORT_USERS_PROJECT_ACCESS_TOKEN, f"teams/{team.name}/{environment_type.value}.yml")
                # If for some reason the file does not exist, skip
                if not environment_file:
                    self.logger.error(f"{environment_type.value}.yml not found in {team.name}")
                    continue
                user_list = yaml.safe_load(environment_file)[team.name]["user_list"]
                # If for some reason 'user_list' does not exist or is invalid, skip this file
                if not user_list:
                    self.logger.error(f"'user_list' not found in {team.name}/{environment_type.value}.yml")
                    continue
                # Iterate through each PID in the user_list
                for pid in user_list:
                    pids_from_gl[environment_type][pid["uid"]] = {
                        "name": pid["name"],
                        "comment": pid["comment"],
                        "team_id": team.id
                    }
        
        # First, check if any PIDs in the database no longer appear in GitLab
        for pid in pids:
            found_pid = False
            for environment_type in pids_from_gl:
                if pid in pids_from_gl[environment_type]:
                    found_pid = True
                    break
            pid.exists_in_gl = found_pid

        # Second, iterate through the PIDs from GitLab and create them if they don't exist in the database
        for environment_type in PIDEnvironmentType:
            for uid in pids_from_gl[environment_type]:
                if not next((pid for pid in pids if pid.uid == uid), None):
                    pid = PID(
                        uid = uid,
                        name = pids_from_gl[environment_type][uid]["name"],
                        comment = pids_from_gl[environment_type][uid]["comment"],
                        team_id = pids_from_gl[environment_type][uid]["team_id"],
                        environment_type = environment_type
                    )
                    self.session.add(pid)
                    self.logger.info(f"Creating {pid}")

        # Save all changes to the database
        self.session.commit()