from access_flow.views.dashboard import DashboardView
from access_flow.views.requests import RequestsView
from access_flow.views.authentication.login import LoginView
from access_flow.views.authentication.logout import LogoutView
from access_flow.views.directory.users import DirectoryUsersView
from access_flow.views.directory.groups import DirectoryGroupsView
from access_flow.views.directory.services import DirectoryServicesView
from access_flow.views.administration.users import AdministrationUsersView
from access_flow.views.administration.logs import AdministrationLogsView
from access_flow import app

app.add_url_rule("/dashboard", view_func = DashboardView.as_view("dashboard"))
app.add_url_rule("/requests", view_func = RequestsView.as_view("requests"))

app.add_url_rule("/login", view_func = LoginView.as_view("login"))
app.add_url_rule("/logout", view_func = LogoutView.as_view("logout"))

app.add_url_rule("/directory/users", view_func = DirectoryUsersView.as_view("directory/users"))
app.add_url_rule("/directory/groups", view_func = DirectoryGroupsView.as_view("directory/groups"))
app.add_url_rule("/directory/services", view_func = DirectoryServicesView.as_view("directory/services"))

app.add_url_rule("/administration/users", view_func = AdministrationUsersView.as_view("administration/users"))
app.add_url_rule("/administration/logs", view_func = AdministrationLogsView.as_view("administration/logs"))