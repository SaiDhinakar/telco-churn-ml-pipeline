import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup a logger; creates logs/ directory if it doesn't exist."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(os.path.join('logs', log_file))        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
