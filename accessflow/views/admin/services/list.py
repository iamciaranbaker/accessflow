from flask import request, redirect, url_for, render_template
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.service import Service

class AdminServiceListView(View):
    methods = ["GET"]
    decorators = [permission_required("list_services"), login_required]

    def dispatch_request(self):
        services = Service.query

        # Check if a search query parameter is present
        search = request.args.get("q")
        # Check if search query parameter is empty, i.e. empty search field submitted
        if search is not None and not search.strip():
            # Redirect to base services page for cleaner URL
            return redirect(url_for("admin/services"))
        if search:
            # Allow the query to search for anything containing the search term
            search = f"%{search}%"
            # Filter against name
            services = services.filter(
                Service.name.like(search)
            )

        # Paginate the returned services
        services = services.paginate(per_page = None if request.args.get("per_page") else 8, max_per_page = 30)

        return render_template("pages/admin/services/list.html", services = services)