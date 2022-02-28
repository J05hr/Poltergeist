import time
import logging
from Poltergeist.utils import files_util


def new_logger():
    """Create and return a new logger for logging app output to a file"""
    # Get the logger file path.
    log_path = files_util.get_log_dir().joinpath('log.txt')
    files_util.dep_check(log_path)

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


def read_log(log_filename, logger):
    """Try to read the log"""
    try:
        with open(log_filename, "r") as log_file:
            log_text = log_file.read()
        return log_text

    except Exception as e:
        logger.error("Error reading log, " + str(e), exc_info=True)