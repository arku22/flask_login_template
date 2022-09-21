from . import user
from flask import render_template
from flask_login import login_required, current_user
from .forms import ChangePassword


@user.route("/home")
@login_required
def user_home():
    return render_template("user/user_home.html", user=current_user)


@user.route("/change_password")
@login_required
def change_password():
    form = ChangePassword()
    return render_template("user/change_password.html", form=form, user=current_user)