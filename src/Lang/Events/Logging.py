from Proxy import EventReceiver, EventProxy
from Lang.FuncTools.Abstraction import abstractmethod

class Severity:
	INFO = 0
	WARNING = 1
	ERROR = 2
	@classmethod
	def asString(cls, numLevel):
		return {cls.INFO:"Info", cls.WARNING:"Warning", cls.ERROR:"Error"}[numLevel]

class LoggerAbstract(EventReceiver):
	def __init__(self):
		super(LoggerAbstract, self).__init__()
		self.minSeverity = Severity.INFO
		self.execLevel = 0
	
	def write(self, message, severity, *args):
		"""
		Write a message to the log
		@param *args:	Additional arguments passed to _write() for subclasses
		"""
		if severity >= self.minSeverity:
			self._write(message, severity, *args)
	@abstractmethod
	def _write(self, message, severity, *args):
		pass

class StdoutLogger(LoggerAbstract):
	"""Logs messages to sys.stdout"""
	def __init__(self):
		super(StdoutLogger, self).__init__()
	def _write(self, message, severity):
		print("\t" * self.execLevel + message)

class Logging(EventProxy):
	"""
	Provides logging messages to one or more loggers.
	
	Just call this class with your event notification methods which are defined in your Logger subclasses. Every logger
	will then be called with that method and its arguments.
	"""
	Severity = Severity
	def __init__(self, loggers):
		super(Logging, self).__init__(errorOnMethodNotFound=False)
		if not hasattr(loggers, "__iter__"):
			loggers = tuple(loggers)
		for logger in loggers:
			self.addReceiver(logger, errorOnDuplicate=True)
	def addReceiver(self, receiver, errorOnDuplicate=True):
		assert isinstance(receiver, LoggerAbstract)
		super(Logging, self).addReceiver(receiver, errorOnDuplicate=errorOnDuplicate)

