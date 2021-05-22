from .Logger import Logger

class LoggerFactory(object):
    def __init__(self):
        super(LoggerFactory, self).__init__()

    def getLogger(self):
        logger = Logger()
        return logger
