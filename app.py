from flask import Flask, render_template
from flask_wtf import FlaskForm
from dotenv import load_dotenv
import os
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

app = Flask(__name__)

# configs
app.config["SECRET_KEY"] = os.environ.get("secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.environ.get('db_username')}:" \
                                        f"{os.environ.get('db_password')}@"    \
                                        f"{os.environ.get('db_hostname')}/"    \
                                        f"{os.environ.get('db_name')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# extension inits
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


# create 'users' table
class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    registration_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    account_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    # foreign key linking
    access_instances = db.relationship("UserAccess", backref="user")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def verify_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def __repr__(self):
        return f"user_id={self.user_id}; email={self.email}; Name={self.last_name}, {self.first_name}"


# create 'user_access table
class UserAccess(db.Model):
    __tablename__ = "user_access"
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    access_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"user_id={self.user_id}; Name={self.user.last_name}, {self.user.first_name}"


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()
    return render_template("register.html", form=form)
