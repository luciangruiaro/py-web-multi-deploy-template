import yaml
import os


class ConfigLoader:
    _config = None

    @classmethod
    def get_config(cls, path="config/config.yaml"):
        if cls._config is None:
            with open(path, 'r') as file:
                cls._config = yaml.safe_load(file)
        return cls._config
