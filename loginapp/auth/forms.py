from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
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