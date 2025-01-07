from flask import request, session, flash, redirect, url_for, render_template
from flask.views import View
from flask_login import current_user, login_user
from accessflow.forms.user import TwoFactorForm
from accessflow.models.user import User

class LoginTwoFactorView(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if not session.get("email_address"):
            return redirect(url_for("login"))

        form = TwoFactorForm(request.form)

        if request.method == "POST":
            if form.validate_on_submit():
                user = User.query.filter_by(email_address = session["email_address"]).first()

                if user and user.verify_two_factor(form.code.data):
                    session.pop("email_address")

                    login_user(user)

                    try:
                        destination = url_for(request.args.get("next"))
                    except:
                        destination = url_for("dashboard")

                    return redirect(destination)
                else:
                    flash("Your two-factor code is invalid.", "danger")

                    form.code.data = None
            else:
                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, "danger")

        return render_template("pages/auth/two_factor.html", form = form)