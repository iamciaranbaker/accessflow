import requests
import urllib.parse
from accessflow.config import Config

class GitLabHandler:
    def get_api_url(self, path):
        return f"{Config.GITLAB_URL}/api/v4/{path}"

    def validate_project_access_token(self, project_url, project_access_token):
        # GitLab API endpoint to check the project access token
        url = self.get_api_url(f"projects/{urllib.parse.quote_plus(project_url)}/access_tokens")

        # Temporary whilst in local development
        proxies = {
            "http": f"socks5h://localhost:1337",
            "https": f"socks5h://localhost:1337"
        }

        response = requests.get(url, headers = {'Private-Token': project_access_token}, proxies = proxies)
        
        if response.status_code == 200:
            data = response.json()
        elif response.status_code == 404:
            return False, "Project or token not found."
        else:
            return False, f"Error: {response.status_code} - {response.text}"