from flask import request, session, flash, redirect, url_for, render_template
from flask.views import View
from flask_login import current_user, login_user
from accessflow.forms.user import LoginForm
from accessflow.models.user import User

class AdminLoginView(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for("admin/index"))
        
        if session.get("email_address"):
            session.pop("email_address")

        form = LoginForm(request.form)

        if request.method == "POST":
            # If the login form passes the validation
            if form.validate_on_submit():
                # Try and obtain the user from the database using the username provided
                user = User.query.filter(User.email_address == form.email_address.data).first()
                
                # Check if a user is returned and the password matches what the user has entered
                if user and user.verify_password(form.password.data):
                    # Check if the user has two-factor authentication enabled
                    if user.has_two_factor:
                        # Set the username in the session so we know who is trying to login on the two-factor page
                        session["email_address"] = user.email_address

                        # Redirect the user to the two-factor authentication page
                        return redirect(url_for("admin/login/two-factor", next = request.args.get("next")))
                    
                    # If the user doesn't have two-factor authentication enabled, log them in
                    login_user(user)

                    # Check if the user needs to be redirected anywhere after login
                    try:
                        destination = url_for(f"{request.args.get("next").strip("/")}")
                    except:
                        destination = url_for("admin/index")

                    return redirect(destination)
                else:
                    # Either a user wasn't found in the database, or the password was incorrect
                    flash("Invalid email address or password.", "danger")
                    form.email_address.errors.append("Invalid email address or password.")
                    form.password.errors.append("Invalid email address or password.")
            else:
                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, "danger")

        return render_template("pages/admin/authentication/login.html", form = form)