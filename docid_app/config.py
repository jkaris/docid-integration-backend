import os


class BaseConfig:
    """Base config class"""
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "9673acd10aa2e08ebbc99ccc5f39d7f3d81c9118c8c6e153cf2badcaf84b12b4")
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(BaseConfig):
    """Production specific config"""
    DEBUG = False
    SECRET_KEY = open('/path/to/secret/file').read()
    ENVIRONMENT = "production"


class StagingConfig(BaseConfig):
    """Staging specific config"""
    ENVIRONMENT = "staging"
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """Development environment specific config"""
    ENVIRONMENT = "development"
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "1745f9fbbb8fe78bf5edc6068274ff662082900d72bd1916f2199fc98a992c37")
