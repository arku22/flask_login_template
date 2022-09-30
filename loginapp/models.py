from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from loginapp import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


# create 'users' table
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
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

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"confirm": self.user_id}).decode("utf-8")

    def confirm_user(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("confirm") != self.user_id:
            return False
        self.account_confirmed = True
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"email_change": self.user_id, "new_email": new_email}).decode("utf-8")

    def email_change(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("email_change") != self.user_id or data.get("new_email") is None:
            return False
        self.email = data.get("new_email")
        db.session.add(self)
        return True

    def generate_pw_reset_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"reset_pw": self.user_id}).decode("utf-8")

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        # get user using payload
        user = Users.query.get(data.get("reset_pw"))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"user_id={self.user_id}; email={self.email}; Name={self.last_name}, {self.first_name}"


# create 'user_access table
class UserAccess(UserMixin, db.Model):
    __tablename__ = "user_access"
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    access_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def get_id(self):
        return self.record_id

    def __repr__(self):
        return f"user_id={self.user_id}; Name={self.user.last_name}, {self.user.first_name}"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
