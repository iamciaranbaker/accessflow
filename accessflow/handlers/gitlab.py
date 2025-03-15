import requests
import urllib.parse
from accessflow.config import Config

class GitLabHandler:
    def get_api_url(self, path):
        return f"{Config.GITLAB_URL}/api/v4/{path}"
    
    def make_api_request(self, api_url, project_access_token, type = "GET", data = {}):
        # If configured, use a proxy for any requests to GitLab
        proxies = None
        if Config.GITLAB_PROXY:
            proxies = {
                "http": Config.GITLAB_PROXY,
                "https": Config.GITLAB_PROXY
            }
        # GitLab requires authentication via a header
        headers = {
            "Private-Token": project_access_token
        }

        if type == "GET":
            return requests.get(api_url, headers = headers, proxies = proxies)
        elif type == "POST":
            return requests.post(api_url, headers = headers, proxies = proxies, data = data)
    
    def sanitize_project_url(self, project_url, url_encode = True):
        # If the GitLab URL is present, remove it
        if Config.GITLAB_URL in project_url:
            project_url = project_url.replace(Config.GITLAB_URL, "")
        # If the project URL starts with a slash, remove it
        if project_url.startswith("/"):
            project_url = project_url[1:]
        # Convert the project URL to a URL encoded string
        if url_encode:
            project_url = urllib.parse.quote_plus(project_url)
        return project_url

    def validate_project_access_token(self, project_url, project_access_token):
        # Sanitize the project URL before use
        project_url = self.sanitize_project_url(project_url)

        # First, make a request to the user endpoint to gather information about the PAT
        user_endpoint_response = self.make_api_request(self.get_api_url("user"), project_access_token)
        # If a 200 status code isn't reported, then the provided PAT isn't valid
        if user_endpoint_response.status_code != 200:
            return False
        
        user_endpoint_response_json = user_endpoint_response.json()
        
        # Ensure the provided PAT is definitely a project token not a personal one
        if not user_endpoint_response_json["bot"]:
            return False
        # Ensure the PAT is active
        if user_endpoint_response_json["state"] != "active":
            return False
        
        # Get the ID of the user created by the PAT
        pat_user_id = user_endpoint_response_json["id"]
        
        # Second, make a request to the project access tokens endpoint
        project_access_tokens_endpoint_response = self.make_api_request(self.get_api_url(f"projects/{project_url}/access_tokens"), project_access_token)
        # If a 200 status code isn't reported, then the provided PAT isn't valid
        if project_access_tokens_endpoint_response.status_code != 200:
            return False
        
        project_access_tokens_endpoint_response_json = project_access_tokens_endpoint_response.json()
        project_access_token_found = False

        for token in project_access_tokens_endpoint_response_json:
            # We only want the active token, not any expired or revoked ones
            # We also only want the token if the user ID matches the one from the user endpoint
            if token["active"] and not token["revoked"] and token["user_id"] == pat_user_id:
                project_access_tokens_endpoint_response_json = token
                project_access_token_found = True

        # Ensure there is a valid PAT found from the project access tokens endpoint
        if not project_access_token_found:
            return False
        
        # Last but not least, for a final verification, make a request to the personal access tokens endpoint
        personal_access_tokens_endpoint_response = self.make_api_request(self.get_api_url("personal_access_tokens"), project_access_token)
        # If a 200 status code isn't reported, then the provided PAT isn't valid
        if personal_access_tokens_endpoint_response.status_code != 200:
            return False
        
        personal_access_tokens_endpoint_response_json = personal_access_tokens_endpoint_response.json()
        personal_access_token_found = False

        for token in personal_access_tokens_endpoint_response_json:
            # We only want the active token, not any expired or revoked ones
            # We also only want the token if the user ID matches the one from the user endpoint
            if token["active"] and not token["revoked"] and token["user_id"] == pat_user_id:
                personal_access_tokens_endpoint_response_json = token
                personal_access_token_found = True
        
        # Ensure there is a valid PAT found from the personal access tokens endpoint
        if not personal_access_token_found:
            return False
        
        # One final check to ensure the found project access token and personal access token match
        if project_access_tokens_endpoint_response_json["id"] != personal_access_tokens_endpoint_response_json["id"]:
            return False

        return True