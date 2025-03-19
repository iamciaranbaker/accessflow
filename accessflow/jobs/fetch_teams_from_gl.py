from accessflow.config import Config
from accessflow import db, gitlab_handler

class FetchTeamsFromGL:
    def run(self):
        teams = gitlab_handler.get_project_repository_tree(Config.SUPPORT_USERS_PROJECT_URL, Config.SUPPORT_USERS_PROJECT_ACCESS_TOKEN, "teams/")