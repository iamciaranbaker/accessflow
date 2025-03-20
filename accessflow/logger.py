import logging

logging.SUCCESS = 25 # Between WARNING and INFO
logging.addLevelName(logging.SUCCESS, "SUCCESS")

class CustomLogFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[0;32m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    format = "%(asctime)s - [ %(levelname)s ] - %(message)s"

    formats = {
        logging.DEBUG: grey + format + reset,
        logging.SUCCESS: green + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_format = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)

def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    setattr(logger, "success", lambda message, *args: logger._log(logging.SUCCESS, message, args))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(CustomLogFormatter())

    logger.addHandler(console_handler)

    return logger