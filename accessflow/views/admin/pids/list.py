from flask import request, redirect, url_for, render_template
from flask.views import View
from flask_login import login_required
from sqlalchemy.orm import joinedload
from accessflow.decorators import permission_required
from accessflow.models.pid import PID
from accessflow.models.team import Team

class AdminPIDListView(View):
    methods = ["GET"]
    decorators = [login_required]

    def dispatch_request(self):
        pids = PID.query.options(joinedload(PID.team)).join(Team)

        # Check if a search query parameter is present
        search = request.args.get("q")
        # Check if search query parameter is empty, i.e. empty search field submitted
        if search is not None and not search.strip():
            # Redirect to base PIDs page for cleaner URL
            return redirect(url_for("admin/pids"))
        if search:
            # Allow the query to search for anything containing the search term
            search = f"%{search}%"
            # Filter against UID, name, comment and team
            pids = pids.filter(
                PID.uid.like(search) |
                PID.name.like(search) |
                PID.comment.like(search) |
                Team.name.like(search)
            )

        # Check if a filter has been applied for team
        filtered_teams = request.args.getlist("filter[team]")
        if filtered_teams:
            pids = pids.filter(Team.name.in_(filtered_teams))

        # Check if a filter has been applied for environment
        filtered_environments = request.args.getlist("filter[environment]")
        if filtered_environments:
            pids = pids.filter(PID.environment_type.in_(filtered_environments))
        
        # Paginate the returned PIDs
        pids = pids.paginate(per_page = None if request.args.get("per_page") else 8, max_per_page = 30)
        
        return render_template("pages/admin/pids/list.html", pids = pids)