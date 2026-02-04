import logging
from ..config import load_config
from pathlib import Path


def setup_logging():
    """Configure logging for the entire application."""
    config = load_config()
    log_level = getattr(logging, config['log'].get('level', 'INFO'))
    Path(config["log"]["logs_dir"]).mkdir(parents=True, exist_ok=True)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{config['log']['logs_dir']}/{config['log']['logs_filename']}"),
            logging.StreamHandler()
        ]
    )