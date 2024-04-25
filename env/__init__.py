"""
A package declares environment variables used by the app.
"""
import logging

from common.logging import Logging
from msg import Msg

#
# For the logging
FILELOGGER: str = 'FileLogger'
LOGFILE: str = '.\\log\\charana-backend.log'

#
# For error handling
MSGFILE: str = '.\\metadata\\msg.csv'

#
# For logging
LOGDEBUG: int = logging.DEBUG
LOGINFO: int = logging.INFO
LOGWARNING: int = logging.WARNING
LOGERROR: int = logging.ERROR
LOGCRITICAL: int = logging.CRITICAL
LOGFATAL: int = logging.FATAL

#
# Data formats
DATAFMT = {
    'LIST': 'LIST',
    'DICT': 'DICTIONARY'
}

class Config(object):
    """
        A class designed for Flask configuration. Be noticed that the
        configuration values shall be updated properly when the app is
        moved to production.
    """
    #
    # class variables for Flask configuration
    DEBUG = True
    TESTING = False

    USETESTDATA = True

    def __init__(self):
        #
        # Initialize the message class
        Config.msginstance = Msg()

        #
        # Initialize the file logger
        Config.loginstance = Logging()
        Logging.SetLevel(LOGDEBUG)
