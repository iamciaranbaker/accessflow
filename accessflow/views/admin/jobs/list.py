from flask import request, redirect, url_for, render_template
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.job import Job

class AdminJobListView(View):
    methods = ["GET"]
    decorators = [permission_required("list_jobs"), login_required]

    def dispatch_request(self):
        jobs = Job.query

        # Check if a search query parameter is present
        search = request.args.get("q")
        # Check if search query parameter is empty, i.e. empty search field submitted
        if search is not None and not search.strip():
            # Redirect to base jobs page for cleaner URL
            return redirect(url_for("admin/jobs"))
        if search:
            # Allow the query to search for anything containing the search term
            search = f"%{search}%"
            # Filter against name
            jobs = jobs.filter(
                Job.name.like(search)
            )

        # Check if a filter has been applied for type
        filtered_types = request.args.getlist("filter[type]")
        if filtered_types:
            jobs = jobs.filter(Job.type.in_(filtered_types))
        
        # Paginate the returned jobs
        jobs = jobs.paginate(per_page = None if request.args.get("per_page") else 8, max_per_page = 30)

        # Create map of filtering options
        filter_options = {
            "types": [
                {
                    "value": "schedule",
                    "label": "Schedule"
                },
                {
                    "value": "trigger",
                    "label": "Trigger"
                }
            ]
        }

        return render_template("pages/admin/jobs/list.html", jobs = jobs, filter_options = filter_options)