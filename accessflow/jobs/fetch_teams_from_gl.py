from accessflow.models.team import Team
from accessflow.config import Config
from accessflow import gitlab_handler

class FetchTeamsFromGL:
    def __init__(self, logger, session):
        self.logger = logger
        self.session = session

    def run(self):
        # Get teams from database
        teams = self.session.query(Team).all()
        # Keep track of teams from GitLab
        teams_from_gl = [team["name"] for team in gitlab_handler.get_project_repository_tree(Config.SUPPORT_USERS_PROJECT_URL, Config.SUPPORT_USERS_PROJECT_ACCESS_TOKEN, "teams")]

        # First, check if any teams in the database no longer appear in GitLab
        for team in teams:
            team.exists_in_gl = team.name in teams_from_gl

        # Second, iterate through the teams from GitLab and create them if they don't exist in the database
        for team_name in teams_from_gl:
            if not next((team for team in teams if team.name == team_name), None):
                team = Team(
                    name = team_name,
                    friendly_name = self.get_friendly_name(team_name)
                )
                self.session.add(team)
                self.logger.info(f"Creating {team}")

        self.session.commit()

    def get_friendly_name(self, name):
        # Define a list of words to exclude from acronym capitalisation
        excluded_acronym_words = ["core"]
        friendly_name = ""
        for word in name.split("_"):
            word = word.lower()
            # If the word is 4 characters or less, it's probably an acronym.
            # Unless it's in the excluded list, capitalise the word
            if len(word) <= 4 and word not in excluded_acronym_words:
                word = word.upper()
            else:
                word = word.title()
            friendly_name += f"{word} "
        return friendly_name.strip()