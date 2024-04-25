import logging
import env

class Logging:
    """
    A logging class configures a file logger for the app.
    """

    __logger = None

    def __init__(self):
        #
        # configure a file logger
        filelogger = env.FILELOGGER

        format = '%(asctime)s %(levelname)s [%(threadName)s] [%(module)s] [%(funcName)s]: %(message)s'
        Logging.__logger = logging.getLogger(filelogger)
        handler = logging.FileHandler(filename=env.LOGFILE, mode='ta')
        fmt = logging.Formatter(format)
        handler.setFormatter(fmt=fmt)
        Logging.__logger.addHandler(handler)
        Logging.__logger.setLevel(logging.DEBUG)

    @classmethod
    def GetLogger(cls):
        """
        Get the file logger.
        :param: None
        :return: the file logger
        """
        return cls.__logger

    @classmethod
    def SetLevel(cls, level = logging.WARNING):
        """
        Set the logging level.
        :param: level: int. It is set logging.WARNING by default if not specified.
        :return: None
        """
        cls.__logger.setLevel(level)
