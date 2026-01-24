import yaml
from pathlib import Path

def load_config():
    """Load configuration from config.yaml"""

    config_path = Path(__file__).parent.parent / "config" / "config.yaml"

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config