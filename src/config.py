import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "techflow_secret_key_validation")
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
