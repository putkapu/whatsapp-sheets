import logging
import os
from typing import Dict, Any


class BaseConfig:
    """Base configuration."""

    # Flask
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

    # Logging
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Google Sheets
    GOOGLE_CREDENTIALS_PATH = os.environ.get("GOOGLE_CREDENTIALS_PATH")
    GOOGLE_SPREADSHEET_ID = os.environ.get("GOOGLE_SPREADSHEET_ID")
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def validate_config(cls) -> None:
        """Validate that all required environment variables are set."""
        required_vars = {
            "FLASK_SECRET_KEY": cls.SECRET_KEY,
            "GOOGLE_CREDENTIALS_PATH": cls.GOOGLE_CREDENTIALS_PATH,
            "GOOGLE_SPREADSHEET_ID": cls.GOOGLE_SPREADSHEET_ID,
            "SQLALCHEMY_DATABASE_URI": cls.SQLALCHEMY_DATABASE_URI,
            "GOOGLE_CLIENT_ID": cls.GOOGLE_CLIENT_ID,
            "GOOGLE_CLIENT_SECRET": cls.GOOGLE_CLIENT_SECRET,
            "GOOGLE_REDIRECT_URI": cls.GOOGLE_REDIRECT_URI,
        }

        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-key-for-testing")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///whatssheet.db"
    )
    GOOGLE_CREDENTIALS_PATH = os.environ.get(
        "GOOGLE_CREDENTIALS_PATH", "credentials.json"
    )
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    DEBUG = True
    SECRET_KEY = "test-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    GOOGLE_CLIENT_ID = "test-client-id"
    GOOGLE_CLIENT_SECRET = "test-client-secret"
    GOOGLE_REDIRECT_URI = "http://localhost:5000/oauth2callback"


class ProductionConfig(BaseConfig):
    """Production configuration."""

    LOG_LEVEL = logging.WARNING

    @classmethod
    def validate_config(cls) -> None:
        super().validate_config()
        if cls.SECRET_KEY == "dev-key-for-testing":
            raise ValueError("Production environment cannot use development secret key")


def get_config() -> Dict[str, Any]:
    """Return the appropriate configuration object based on the environment."""
    env = os.environ.get("FLASK_ENV", "development").lower()

    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    config_class = configs.get(env)
    if not config_class:
        raise ValueError(f"Invalid environment: {env}")

    if env == "production":
        config_class.validate_config()

    return config_class

Config = get_config()
