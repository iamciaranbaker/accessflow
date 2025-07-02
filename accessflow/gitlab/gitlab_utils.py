from flask import current_app
from accessflow.config import Config
import requests
import urllib.parse
import hashlib
import json

def make_api_url(path):
    return f"{Config.GITLAB_URL}/api/v4/{path}"

def make_api_cache_key(api_url, project_access_token, params):
    key = json.dumps({
        "api_url": api_url,
        "project_access_token": project_access_token,
        "params": params
    }, sort_keys = True)
    return hashlib.md5(key.encode("utf-8")).hexdigest()

def make_api_request(api_url, project_access_token, type = "GET", data = None, params = None):
    cache = current_app.cache

    if type == "GET":
        cache_key = make_api_cache_key(api_url, project_access_token, params)
        cached_data = cache.get(cache_key)
        # Check if response is already available in cache
        if cached_data:
            response = requests.Response()
            response.status_code = cached_data["status_code"]
            response._content = cached_data["content"].encode("utf-8")
            response.headers = cached_data["headers"]
            return response
            
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

    api_url = make_api_url(api_url)

    if type == "GET":
        response = requests.get(api_url, headers = headers, proxies = proxies, params = params)

        # Cache response for 30 seconds to reduce both load on GitLab and waiting times
        cache.set(cache_key, {
            "status_code": response.status_code,
            "content": response.text,
            "headers": dict(response.headers),
        }, timeout = 30)

        return response
    elif type == "POST":
        return requests.post(api_url, headers = headers, proxies = proxies, data = data, params = params)

def sanitize_project_url(project_url, url_encode = True):
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