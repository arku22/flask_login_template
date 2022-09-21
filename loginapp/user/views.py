from . import user
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import ChangePassword
from ..models import db


@user.route("/home")
@login_required
def user_home():
    return render_template("user/user_home.html", user=current_user)


@user.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        old_pw = form.old_password.data
        if not current_user.verify_password(old_pw):
            flash("Incorrect password entered! Please try again.")
            return redirect(url_for("user.change_password"))
        current_user.password = form.new_password.data
        db.session.add(current_user)
        db.session.commit()
        flash("Password changed successfully!")
        return redirect(url_for('user.user_home'))
    return render_template("user/change_password.html", form=form)
