##########################################################
###                                                    ###
###                Coloured logger                     ###
###                                                    ###
###                Date: 05/11/2025                    ###
###                                                    ###
##########################################################
import logging
import sys


# Gestion des couleurs et du niveau
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\x1b[36m',   # Cyan
        'INFO': '\x1b[0m',     # Default
        'WARNING': '\x1b[33m', # Yellow
        'ERROR': '\x1b[31m',   # Red
    }

    RESET = '\x1b[0m'

    def format(self, record):
        levelname = record.levelname
        color = self.COLORS.get(levelname, self.RESET)
        message = super().format(record)
        return f"{color}{levelname:<7}: {message}{self.RESET}"


# Initialisation du logger
def Init(LoggerStream=sys.stdout, level=logging.INFO):
    logger = logging.getLogger("mylogger")
    logger.setLevel(level)
    logger.propagate = False

    # Remove old handlers (useful for repeated calls)
    for hdlr in list(logger.handlers):
        logger.removeHandler(hdlr)

    # Create stream handler
    handler = logging.StreamHandler(LoggerStream)
    formatter = ColoredFormatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

