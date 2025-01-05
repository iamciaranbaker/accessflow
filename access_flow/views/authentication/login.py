from flask import request, session, flash, redirect, url_for, render_template
from flask.views import View
from flask_login import current_user, login_user
from access_flow.forms.user import LoginForm
from access_flow.models.user import User

class LoginView(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        
        if session.get("username"):
            session.pop("username")

        form = LoginForm(request.form)
        autofocus = "username"

        if request.method == "POST":
            # If the login form passes the validation.
            if form.validate_on_submit():
                # Try and obtain the user from the database using the username provided.
                user = User.query.filter_by(username = form.username.data).first()
                
                # Check if a user is returned and the password matches what the user has entered.
                if user and user.verify_password(form.password.data):
                    # Check if the user has two-factor authentication enabled.
                    if user.has_two_factor:
                        # Set the username in the session so we know who is trying to login on the two-factor page.
                        session["username"] = user.username

                        # Redirect the user to the two-factor authentication page.
                        return redirect(url_for("login/two-factor"))
                    
                    # If the user doesn't have two-factor authentication enabled, log them in.
                    login_user(user)

                    # Check if the user needs to be redirected anywhere after login.
                    try:
                        destination = url_for(request.args.get("next"))
                    except:
                        destination = url_for("dashboard")

                    return redirect(destination)
                else:
                    # Either a user wasn't found in the database, or the password was incorrect.
                    flash("Invalid username or password.", "danger")
            else:
                # Find the first field with a validation error and set the autofocus to this for better UI experience.
                autofocus = list(form.errors.keys())[0]

                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, "danger")

        return render_template("pages/authentication/login.html", form = form, autofocus = autofocus)