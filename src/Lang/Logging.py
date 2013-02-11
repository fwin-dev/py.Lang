from . import abstractmethod
import sys

class Severity:
	INFO = 0
	WARNING = 1
	ERROR = 2
	@classmethod
	def asString(cls, numLevel):
		return {cls.INFO:"Info", cls.WARNING:"Warning", cls.ERROR:"Error"}[numLevel]

class LoggerAbstract(object):
	def __init__(self):
		self.minSeverity = Severity.INFO
		self.execLevel = 0
	def notifyException(self, exceptionClass, exceptionInstance, tracebackInstance):
		"""
		@param exceptionClass:		The exception class/type of the instance
		@param tracebackInstance:	Suitable for passing into the builtin python function traceback.format_tb
		"""
		pass
	
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
	def write(self, message, severity):
		print("\t" * self.execLevel + message)

class Logging:
	"""
	Provides logging messages to one or more loggers.
	
	Just call this class with your event notification methods which are defined in your Logger subclasses. Every logger
	will then be called with that method and its arguments.
	"""
	Severity = Severity
	def __init__(self, loggers):
		self.loggers = loggers
		if not hasattr(self.loggers, "__iter__"):
			self.loggers = tuple(self.loggers)
		for logger in loggers:
			assert isinstance(logger, LoggerAbstract)
		
		oldFunc = sys.excepthook
		def branchHook(exceptionClass, exceptionInstance, tracebackInstance):
			oldFunc(exceptionClass, exceptionInstance, tracebackInstance)
			self.notifyException(exceptionClass, exceptionInstance, tracebackInstance)
		sys.excepthook = branchHook
	
	def __getattr__(self, name):
		def _run(*args, **kwargs):
			found = False
			for logger in self.loggers:
				if hasattr(logger, name):
					found = True
					getattr(logger, name)(*args, **kwargs)
			if not found:
				if name != "notifyException":
					raise AttributeError
		return _run

