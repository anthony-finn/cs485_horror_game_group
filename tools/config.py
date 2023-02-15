import yaml
from os import path

PROJECT_ROOT = path.abspath(path.dirname(__file__) + "/..") + "/"

# Load YML Configurations
yml_configs = {}

with open(PROJECT_ROOT + 'config.yml', 'r') as config:
    yml_configs = yaml.safe_load(config)

def file_to_str(filename: str) -> str:
    return ''.join(
        open(PROJECT_ROOT + f"data/{filename}", "r")
            .readlines())
