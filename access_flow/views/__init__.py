from access_flow.views.dashboard import DashboardView
from access_flow import app

app.add_url_rule('/', view_func = DashboardView.as_view('dashboard'))