################################################################################
# Nice colored logger
# Taken from MadAnalysis 5 ;)
################################################################################

import logging
import sys

class ColoredFormatter(logging.Formatter):

    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self,record):
        if   (record.levelno >= 40):   #FATAL
            color = '\x1b[31mERROR  : '
        elif (record.levelno >= 30): #WARNING
            color = '\x1b[35mINFO   : '
        elif (record.levelno >= 20): #INFO
            color = '\x1b[0mINFO   : '
        elif (record.levelno >= 10): #DEBUG
            color = '\x1b[36mDEBUG  : '
        else:                          #ANYTHING ELSE
            color = '\x1b[0m'
        record.msg = color + str( record.msg ) + '\x1b[0m'
        return logging.Formatter.format(self, record)

def Init(LoggerStream=sys.stdout):
    logger = logging.getLogger('mylogger')
    for hdlr in logger.handlers:
        logger.removeHandler(hdlr)
    hdlr = logging.StreamHandler(LoggerStream)
    fmt = ColoredFormatter('%(message)s')
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    logger.propagate=False
    logger.setLevel(logging.INFO)
