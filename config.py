import yaml

def load_config(config_file="config.yaml"):
    """
    Load configuration settings from a YAML file.
    Args:
        config_file (str): Path to the YAML configuration file.
    Returns:
        dict: Dictionary containing the configuration settings.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Example usage
config = load_config("config.yaml")
print(config["excel"]["file_path"])  # Access the Excel file path
