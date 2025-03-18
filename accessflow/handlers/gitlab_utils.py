import requests
import urllib.parse
from accessflow.config import Config

def make_api_url(path):
    return f"{Config.GITLAB_URL}/api/v4/{path}"

def make_api_request(api_url, project_access_token, type = "GET", data = None):
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