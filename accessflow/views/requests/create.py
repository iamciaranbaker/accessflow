from flask import request, render_template
from flask.views import View
from accessflow.forms.request import CreateRequestForm

class RequestCreateView(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = CreateRequestForm(request.form)

        if request.method == "POST":
            print(form.data)
            
        template = "create"
        if request.args.get("poc"):
            template += "_poc"
        return render_template(f"pages/requests/{template}.html", form = form)