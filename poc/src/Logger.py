class Logger(object):
	def __init__(self):
		super(Logger, self).__init__()
	def error(self, message, e):
		error_class = e.__class__.__name__
		detail = e.args[0]
		print("------------error-------------")
		print("{}".format(message))
		print("error type: {}".format(error_class))
		print("{}".format(detail))
		print("------------------------------")