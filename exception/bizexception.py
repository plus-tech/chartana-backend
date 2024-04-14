# Define a businenss logic exception

class BizException(Exception):
    """
        Declare a custom exception dealing with business logic errors in the app.

        :params:
            code: the error code
            message: the descriptive text
    """

    def __init__(self, code, message):
        assert isinstance(code, int)
        assert isinstance(message, str)
        
        self.__code = code
        self.__message = message

    @property
    def code(self):
        return self.__code

    @property
    def message(self):
        return self.__message

    def getcode(self):
        return self.__code

    def getmessage(self):
        return self.__message

    def __str__(self):
        return str(self.__code) + ':' + self.__message

    @code.setter
    def code(self, code):
        self.__code = code

    @message.setter
    def message(self, message):
        self.__message = message
