from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get("PROD_DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = "postgres://hwhhbdiiqspkaw:620334b20c597bfb0a1cc63ac401e0d047ab54059433e92485c89968bdd125c8@ec2-3-229-161-70.compute-1.amazonaws.com:5432/d8dugjqmc1p53s"


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get("DEV_DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = environ.get("DEV_SQLALCHEMY_DATABASE_URI")


class TestConfig(Config):
    FLASK_ENV = "test"
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get("TEST_DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = environ.get("TEST_SQLALCHEMY_DATABASE_URI")
