from .forms import RegistrationForm, LoginForm
from flask import render_template, flash, redirect, url_for, request
from . import auth
from ..models import Users, UserAccess
from loginapp import db
from flask_login import login_user, login_required, logout_user, current_user


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
        flash("You can now login!")
        return redirect(url_for("auth.register_page"))
    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for("auth.register_page"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # log the user in
            login_user(user, form.remember_me.data)
            next_pg = request.args.get("next")
            if next_pg is None or not next_pg.startswith('/'):
                flash("You are logged in!")
                return redirect(url_for("auth.register_page"))
            flash("You are logged in!")
            return redirect(next_pg)
        flash("Incorrect email and/or password!")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
