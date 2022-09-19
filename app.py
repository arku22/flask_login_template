from flask import Flask, render_template
from flask_wtf import FlaskForm
from dotenv import load_dotenv
import os
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, EqualTo


file_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(file_dir)

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("secret_key")


# create a registration form
class RegistrationForm(FlaskForm):

    email = StringField(label="Email",
                        validators=[DataRequired(), Email()])
    first_name = StringField(label="First Name",
                             validators=[DataRequired()])
    last_name = StringField(label="Last Name",
                            validators=[DataRequired()])
    password = PasswordField(label="Password",
                             validators=[DataRequired(), EqualTo("confirm_password", message="Passwords must match!")])
    confirm_password = PasswordField(label="Confirm Password",
                                     validators=[DataRequired()])
    register_btn = SubmitField(label="Register")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()
    return render_template("register.html", form=form)
