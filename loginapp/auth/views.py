from .forms import RegistrationForm, LoginForm
from flask import render_template, flash, redirect, url_for, request
from . import auth
from ..models import Users, UserAccess
from loginapp import db
from flask_login import login_user, login_required, logout_user, current_user
from ..email import send_email


@auth.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        if Users.query.filter_by(email=email).first():
            flash("This email is already in use! Please try another email address or login to your account.")
            return redirect(url_for("auth.register_page"))
        new_user = Users(email=email,
                         first_name=form.first_name.data,
                         last_name=form.last_name.data,
                         password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_confirmation_token()
        send_email(subject="New Account Confirmation",
                   to=new_user.email,
                   txt_body="email/new_user_email.txt",
                   token=token,
                   user=new_user)
        flash("A confirmation email has been sent to your email.")
        return redirect(url_for("auth.register_page"))
    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("user.user_home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # log the user in
            login_user(user, form.remember_me.data)
            next_pg = request.args.get("next")
            if next_pg is None or not next_pg.startswith('/'):
                return redirect(url_for("user.user_home"))
            flash("You are logged in!")
            return redirect(next_pg)
        flash("Incorrect email and/or password!")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("auth.login_page"))


@auth.route("/confirm/<token>")
@login_required
def confirm_user(token):
    # current user already confirmed
    if current_user.account_confirmed:
        flash("Account already confirmed!")
        return redirect(url_for("user.user_home"))
    if current_user.confirm_user(token):
        db.session.commit()
        flash("Your account has been confirmed!")
    else:
        flash("This URL is invalid or expired!")
    return redirect(url_for("user.user_home"))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated  \
            and not current_user.account_confirmed  \
            and request.blueprint != "auth" \
            and request.endpoint != "static":
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.account_confirmed:
        return redirect(url_for("user.user_home"))
    return render_template("auth/confirm.html", user=current_user)


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(subject="New Account Confirmation",
               to=current_user.email,
               txt_body="email/new_user_email.txt",
               token=token,
               user=current_user)
    flash("A new confirmation email has been sent to your email.")
    return redirect(url_for("auth.login_page"))
