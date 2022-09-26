from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Email


class ChangePassword(FlaskForm):

    old_password = PasswordField(label="Old Password",
                                 validators=[DataRequired()])
    new_password = PasswordField(label="New Password",
                                 validators=[DataRequired(), EqualTo("confirm_new_password",
                                                                     message="Passwords must match!")])
    confirm_new_password = PasswordField(label="Confirm New Password",
                                         validators=[DataRequired()])
    submit_btn = SubmitField(label="Change Password")


class ChangeEmail(FlaskForm):

    old_email = StringField(label="Email",
                            validators=[DataRequired(), Email()])
    new_email = StringField(label="New Email",
                            validators=[DataRequired(), Email(), EqualTo("confirm_new_email",
                                                                         message="Recheck entered new email!")])
    confirm_new_email = StringField(label="Confirm New Email",
                                    validators=[DataRequired(), Email()])
    submit_btn = SubmitField(label="Change Email")
