import logging

from termcolor import colored


class ColoredFormatter(logging.Formatter):
    format = "[%(asctime)s] [%(levelname)s] %(message)s"

    FORMATS = {
        logging.DEBUG: colored(format, "yellow"),
        logging.INFO: colored(format, "green"),
        logging.WARNING: colored(format, "cyan"),
        logging.ERROR: colored(format, "magenta"),
        logging.CRITICAL: colored(format, "red"),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%d %b %Y, %I:%M%p")
        return formatter.format(record)
