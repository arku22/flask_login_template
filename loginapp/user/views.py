from . import user
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from .forms import ChangePassword, ChangeEmail
from ..models import db
from ..email import send_email


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


@user.route("/change_email", methods=["GET", "POST"])
@login_required
def request_change_email():
    form = ChangeEmail()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            n_email = form.new_email.data.lower()
            token = current_user.generate_email_change_token(new_email=n_email)
            send_email(subject="Email Address Change Request",
                       to=n_email,
                       txt_body="email/email_change.txt",
                       token=token,
                       user=current_user)
            flash("An email with steps to change your email address was sent to your new email.")
            return redirect(url_for("user.user_home"))
        flash("Invalid email or password")
    return render_template("user/change_email.html", form=form)


@user.route("/change_email/<token>")
@login_required
def change_email(token):
    if current_user.email_change(token):
        db.session.commit()
        flash("Your email has been changed! Please login with your new email id.")
        logout_user()
        return redirect(url_for("auth.login_page"))
    flash("That token is invalid or expired")
    return redirect(url_for("user.user_home"))
