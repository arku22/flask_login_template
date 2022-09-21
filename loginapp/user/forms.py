from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class ChangePassword(FlaskForm):

    old_password = PasswordField(label="Old Password",
                                 validators=[DataRequired()])
    new_password = PasswordField(label="New Password",
                                 validators=[DataRequired(), EqualTo("confirm_new_password",
                                                                     message="Passwords must match!")])
    confirm_new_password = PasswordField(label="Confirm New Password",
                                         validators=[DataRequired()])
    submit_btn = SubmitField(label="Change Password")

