from flask import Flask, render_template


app = Flask(__name__)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    return render_template("register.html")
