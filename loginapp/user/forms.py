from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from ..models import Users


class ChangePassword(FlaskForm):

    old_password = PasswordField(label="Old Password",
                                 validators=[DataRequired()])
    new_password = PasswordField(label="New Password",
                                 validators=[DataRequired(),
                                             EqualTo("confirm_new_password", message="Passwords must match!"),
                                             Length(min=6,
                                                    max=30,
                                                    message="Password must be between 6 & 30 characters long!")
                                             ])
    confirm_new_password = PasswordField(label="Confirm New Password",
                                         validators=[DataRequired()])
    submit_btn = SubmitField(label="Change Password")


class ChangeEmail(FlaskForm):

    new_email = StringField(label="New Email",
                            validators=[DataRequired(), Email()])
    password = PasswordField(label="Password",
                             validators=[DataRequired()])
    submit_btn = SubmitField(label="Change Email")

    def validate_new_email(self, field):
        if Users.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Email already registered!")
