from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired, EqualTo


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


# create a login form
class LoginForm(FlaskForm):

    email = StringField(label="Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField(label="Password",
                             validators=[DataRequired()])
    remember_me = BooleanField(label="Remember me")
    login_btn = SubmitField(label="Sign In")


# create password reset form
class ResetPassword(FlaskForm):

    email = StringField(label="Enter the email associated with your account",
                        validators=[DataRequired(), Email()])
    submit_btn = SubmitField(label="Submit")
