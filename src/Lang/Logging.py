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
		pass
	
	def write(self, message, severity, *args):
		if severity >= self.minSeverity:
			self._write(message, severity, *args)
	@abstractmethod
	def _write(self, message, severity, *args):
		pass

class StdoutLogger(LoggerAbstract):
	def __init__(self):
		super(StdoutLogger, self).__init__()
	def write(self, message, severity):
		print("\t" * self.execLevel + message)

class MySQLloggerAbstract(LoggerAbstract):
	try:
		from Net.DB import MySQL as _MySQL
	except ImportError:
		raise Exception("Install the py.Net.DB.MySQL package via pip to use this logging class")
	
	def __init__(self, host, port, database, username, password):
		super(MySQLloggerAbstract, self).__init__()
		self._db = self._MySQL.Connection(host=host, port=port, database=database, username=username, password=password)


class Logging:
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

