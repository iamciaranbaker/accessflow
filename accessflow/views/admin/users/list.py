from flask import request, redirect, url_for, render_template
from flask.views import View
from flask_login import login_required
from accessflow.decorators import permission_required
from accessflow.models.user import User

class AdminUserListView(View):
    methods = ["GET"]
    decorators = [permission_required("list_users"), login_required]

    def dispatch_request(self):
        users = User.query

        # Check if a search query parameter is present
        search = request.args.get("q")
        # Check if search query parameter is empty, i.e. empty search field submitted
        if search is not None and not search.strip():
            # Redirect to base users page for cleaner URL
            return redirect(url_for("admin/users"))
        if search:
            # Allow the query to search for anything containing the search term
            search = f"%{search}%"
            # Filter against name and email address
            users = users.filter(
                User.first_name.like(search) |
                User.last_name.like(search) |
                User.email_address.like(search)
            )
        
        # Paginate the returned users
        users = users.paginate(per_page = None if request.args.get("per_page") else 8, max_per_page = 30)

        return render_template("pages/admin/users/list.html", users = users)