# --- logger_util.py ---
import logging
import logging.config
import yaml
from pathlib import Path
from logger_context import call_id_var


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.call_id = call_id_var.get()
        return True


def setup_logger(module_name: str, config_path: str = "logging_config.yaml") -> logging.Logger:
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    # Load logging configuration from YAML
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    except FileNotFoundError:
        print(f"Warning: Config file {config_path} not found. Using basic logging configuration.")
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(call_id)s - %(name)s - %(module)s - %(funcName)s:%(lineno)d - %(levelname)s -  %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/BTP-1.log', mode='a', encoding='utf8')
            ]
        )
        # Add context filter to basic handlers
        for handler in logging.getLogger().handlers:
            handler.addFilter(ContextFilter())
    except Exception as e:
        print(f"Error loading logging config: {e}. Using basic configuration.")
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(call_id)s - %(name)s - %(module)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s'
        )
        # Add context filter to basic handlers
        for handler in logging.getLogger().handlers:
            handler.addFilter(ContextFilter())

    return logging.getLogger(module_name)