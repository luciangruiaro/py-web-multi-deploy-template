import os
from config.config_loader import ConfigLoader
from helpers.logger import setup_logger

IS_DOCKER = os.environ.get("ENV") == "DOCKER"

DATA_DIR = "/app/data" if IS_DOCKER else "./data"
LOGS_DIR = "/app/logs" if IS_DOCKER else "./logs"


def ensure_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)


# Call at module import
ensure_directories()
logger = setup_logger("app", log_dir=LOGS_DIR)


def create_app(template_dir=None, static_dir=None):
    config = ConfigLoader().get_config()
    framework = config.get('framework', 'flask').lower()

    if framework == 'flask':
        from api.flask_routes import create_flask_app
        return create_flask_app(config, template_dir, static_dir)

    elif framework == 'fastapi':
        from api.fastapi_routes import create_fastapi_app
        return create_fastapi_app(config)

    else:
        raise ValueError(f"Unsupported framework: {framework}")
