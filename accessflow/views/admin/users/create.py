from flask import request, flash, render_template
from flask.views import View
from flask_login import login_required
from accessflow.forms.user import CreateUserForm

class UserCreateView(View):
    methods = ["GET", "POST"]
    decorators = [login_required]

    def dispatch_request(self):
        form = CreateUserForm(request.form)
        autofocus = "first_name"

        #print(form._fields)

        if request.method == "POST":
            for group in form.permission_groups:
                for permission_field in group["permission_fields"]:
                    print(permission_field.name)
                    print(permission_field.data)

            if form.validate_on_submit():
                pass
            else:
                # Find the first field with a validation error and set the autofocus to this for better UI experience.
                autofocus = list(form.errors.keys())[0]

                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, "danger")

        return render_template("pages/admin/users/create.html", form = form, autofocus = autofocus)