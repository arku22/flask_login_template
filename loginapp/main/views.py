from . import main
from flask import render_template


@main.route("/")
def index():
    return render_template("main/webapp_home.html")


@main.route("/about")
def about():
    return render_template("main/about.html")
