from . import user
from flask import render_template
from flask_login import login_required, current_user


@user.route("/user/home")
@login_required
def user_home():
    return render_template("user/user_home.html", user=current_user)
