class Logger(object):
	def __init__(self):
		super(Logger, self).__init__()
	def error(self, message, exceptionMessage):
		print("{}".format(message));
		print("{}".format(exceptionMessage));