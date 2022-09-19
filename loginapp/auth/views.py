from .forms import RegistrationForm
from flask import render_template, flash, redirect, url_for
from . import auth
from ..models import Users, UserAccess
from loginapp import db


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
    return render_template("register.html", form=form)
