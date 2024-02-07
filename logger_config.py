# logger_config.py
import logging

logger = None

def configure_logger():
    global logger

    # Return the existing logger if it has already been configured
    if logger:
        return logger

    # Configure the root logger
    logging.basicConfig(level=logging.DEBUG)

    # Set the Werkzeug logger level to WARNING
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)

    # Create a logger for your application
    logger = logging.getLogger(__name__)

    # Create a handler to output log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Set the desired log level
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger
