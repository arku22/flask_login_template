from dotenv import load_dotenv
import os


load_dotenv()


class Config:

    SECRET_KEY = os.environ.get("secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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

    
config = {"develop": "DevelopmentConfig",
          "production": "ProductionConfig"}

