import time
import logging
from Poltergeist.utils import dir_util


def new_logger():
    """Create and return a new logger for logging app output to a file"""
    # Get the logger file path.
    log_path = dir_util.get_log_dir().joinpath('log.txt')
    dir_util.dep_check(log_path)

    # Create a custom logger.
    logger = logging.getLogger("logger:"+str(time.time()))

    # Create handlers.
    f_handler = logging.FileHandler(log_path, mode='a')
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers.
    f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)

    # Add handlers to the logger.
    logger.addHandler(f_handler)

    return logger
