import requests
import urllib.parse
from accessflow.config import Config

class GitLabHandler:
    def get_api_url(self, path):
        return f"{Config.GITLAB_URL}/api/v4/{path}"
    
    def sanitize_project_url(self, project_url, url_encode = True):
        if Config.GITLAB_URL in project_url:
            project_url = project_url.replace(Config.GITLAB_URL, "")
        if project_url.startswith("/"):
            project_url = project_url[1:]
        if url_encode:
            project_url = urllib.parse.quote_plus(project_url)
        return project_url

    def validate_project_access_token(self, project_url, project_access_token):
        project_url = self.sanitize_project_url(project_url)
        
        # GitLab API endpoint to check the project access token
        url = self.get_api_url(f"projects/{project_url}/access_tokens")

        # Temporary whilst in local development
        proxies = {
            "http": f"socks5h://localhost:1337",
            "https": f"socks5h://localhost:1337"
        }

        response = requests.get(url, headers = {'Private-Token': project_access_token}, proxies = proxies)
        print(response.text)
        
        if response.status_code == 200:
            data = response.json()
            return True
        elif response.status_code == 404:
            return False
        else:
            return False