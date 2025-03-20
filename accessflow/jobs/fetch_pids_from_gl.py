from accessflow.models.team import Team
from accessflow.models.pid import PID, PIDEnvironmentType
from accessflow.config import Config
from accessflow.logger import logger
from accessflow import db, gitlab_handler
import urllib.parse
import yaml

class FetchPIDsFromGL:
    def run(self):
        # Get teams and PIDs from database
        teams = Team.query.all()
        pids = PID.query.all()
        # Keep track of all PIDs from GitLab and map them to their respective team
        pids_from_gl = {
            "nonprod": {},
            "prod": {}
        }
        # Keep track of the PIDs and map them to the user's name
        pid_name_mapping = {}

        return

        for team in teams:
            for environment_type in ["nonprod", "prod"]:
                environment_file = gitlab_handler.get_project_repository_file(Config.SUPPORT_USERS_PROJECT_URL, Config.SUPPORT_USERS_PROJECT_ACCESS_TOKEN, urllib.parse.quote_plus(f"teams/{team.name}/{environment_type}.yml"))
                # If for some reason the file does not exist, skip
                if not environment_file:
                    logger.error(f"{environment_type}.yml not found in {team.name}")
                    continue
                user_list = yaml.safe_load(environment_file)[team.name]["user_list"]
                # If for some reason 'user_list' does not exist or is invalid, skip this file
                if not user_list:
                    logger.error(f"'user_list' not found in {team.name}/{environment_type}.yml")
                    continue
                # Iterate through each PID in the user_list
                for pid in user_list:
                    pids_from_gl[environment_type][pid["uid"]] = team.id
                    if pid["uid"] in pid_name_mapping:
                        if pid_name_mapping[pid["uid"]] != pid["comment"]:
                            logger.error(f"{pid['uid']} has a name inconsistency: '{pid_name_mapping[pid['uid']]}' vs '{pid['comment']}'")
                    else:
                        pid_name_mapping[pid["uid"]] = pid["comment"]
        
        # First, check if any PIDs in the database no longer appear in GitLab
        for pid in pids:
            pid.exists_in_gl = pid.uid in pids_from_gl["nonprod"] or pid.uid in pids_from_gl["prod"]

        # Second, iterate through the PIDs from GitLab and create them if they don't exist in the database
        for environment_type in ["nonprod", "prod"]:
            for uid in pids_from_gl[environment_type]:
                if not next((pid for pid in pids if pid.uid == uid), None):
                    pid = PID(
                        uid = uid,
                        name = pid_name_mapping[uid],
                        team_id = pids_from_gl[environment_type][uid],
                        environment_type = PIDEnvironmentType.NONPROD if environment_type == "nonprod" else PIDEnvironmentType.PROD
                    )
                    db.session.add(pid)
                    logger.info(f"Creating {pid}")

        # Save all changes to the database
        db.session.commit()