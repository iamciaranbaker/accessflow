from flask import redirect, url_for
from flask.views import View

class IndexView(View):
    methods = ["GET"]

    def dispatch_request(self):
        return redirect(url_for("requests/create"))