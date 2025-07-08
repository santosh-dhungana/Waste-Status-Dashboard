import toml

def load_app_config(config_path="config.toml"):
    return toml.load(config_path)