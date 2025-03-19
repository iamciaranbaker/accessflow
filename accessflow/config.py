import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    # URL of the GitLab instance
    GITLAB_URL = os.getenv("GITLAB_URL")
    GITLAB_PROXY = os.getenv("GITLAB_PROXY")

    # Details of Support Users project, temporary for now
    SUPPORT_USERS_PROJECT_URL = os.getenv("SUPPORT_USERS_PROJECT_URL")
    SUPPORT_USERS_PROJECT_ACCESS_TOKEN = os.getenv("SUPPORT_USERS_PROJECT_ACCESS_TOKEN")

    # MySQL database credentials
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASS = os.getenv("MYSQL_PASS")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"