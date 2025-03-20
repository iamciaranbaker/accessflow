from accessflow.models.team import Team
from accessflow.config import Config
from accessflow import db, gitlab_handler

class FetchTeamsFromGL:
    def __init__(self, logger):
        self.logger = logger

    def run(self):
        # Get teams from database
        teams = Team.query.all()
        # Keep track of teams from GitLab
        teams_from_gl = [team["name"] for team in gitlab_handler.get_project_repository_tree(Config.SUPPORT_USERS_PROJECT_URL, Config.SUPPORT_USERS_PROJECT_ACCESS_TOKEN, "teams")]

        # First, check if any teams in the database no longer appear in GitLab
        for team in teams:
            team.exists_in_gl = team.name in teams_from_gl

        # Second, iterate through the teams from GitLab and create them if they don't exist in the database
        for team_name in teams_from_gl:
            if not next((team for team in teams if team.name == team_name), None):
                team = Team(
                    name = team_name
                )
                db.session.add(team)
                self.logger.info(f"Creating {team}")

        db.session.commit()