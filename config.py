from dotenv import load_dotenv
import os


load_dotenv()


class Config:

    SECRET_KEY = os.environ.get("secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # config to send out email, make changes for your usecase!!
    # this is set for gmail currently
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("email_username")
    MAIL_PASSWORD = os.environt.get("email_password")
    MAIL_SUBJECT_PREFIX = "LoginApp - "
    MAIL_SENDER = os.environ.get("email_address_sender")


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('db_username')}:" \
                              f"{os.environ.get('db_password')}@"    \
                              f"{os.environ.get('db_hostname')}/"    \
                              f"{os.environ.get('prod_db_name')}"


class DevelopmentConfig(Config):

    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('db_username')}:" \
                              f"{os.environ.get('db_password')}@" \
                              f"{os.environ.get('db_hostname')}/" \
                              f"{os.environ.get('dev_db_name')}"


config = {"develop": DevelopmentConfig,
          "production": ProductionConfig}
