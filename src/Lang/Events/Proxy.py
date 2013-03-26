from Lang.Struct import OrderedSet
import sys

class EventReceiver(object):
	"""
	Feel free to use this class as a mixin for receiving specific events.
	
	However, strict use of this class is not necessary. If your class is subscribed to an EventProxy and is not
	a subclass of EventReceiver, your class will still receive any events. Therefore, this class is mainly used
	for code documentation and understandability.
	
	The special method `notifyException(exceptionInstance, tracebackInstance)` can be implemented here which will
	be called when an exception happens. The `tracebackInstance` argument is suitable for passing into the
	builtin python function `traceback.format_tb`.
	"""

class EventProxy(EventReceiver):
	"""
	Any method called on this class (besides reserved functions declared in this class) will be proxied out to all
	EventReceivers registered with the class.
	This class is also an EventReceiver itself, as it receives events. Therefore, multiple EventProxy's can be tied
	together; an event proxy can be registered as an EventReceiver with another EventProxy.
	"""
	def __init__(self, errorOnMethodNotFound):
		"""
		@param errorOnMethodNotFound	bool:	If `True`, it is an error when a receiver doesn't implement a method. If `False`, that receiver is simply skipped. Note that if the special method `notifyException` is not implemented, no error will be raised from this class.
		"""
		self.errorOnMethodNotFound = errorOnMethodNotFound
		self._receivers = OrderedSet()
		self._tieInExceptHook()
	
	def _tieInExceptHook(self):
		oldFunc = sys.excepthook
		def branchHook(exceptionClass, exceptionInstance, tracebackInstance):
			oldFunc(exceptionClass, exceptionInstance, tracebackInstance)
			self.notifyException(exceptionInstance, tracebackInstance)
		sys.excepthook = branchHook
	
	def __getattr__(self, name):
		def _run(*args, **kwargs):
			found = False
			for receiver in self._receivers:
				if hasattr(receiver, name):
					found = True
					getattr(receiver, name)(*args, **kwargs)
			if not found:
				if name != "notifyException" and self.errorOnMethodNotFound:
					raise AttributeError
		return _run
	
	def addReceiver(self, receiver, errorOnDuplicate=True):
		if self._receivers.add(receiver, updateOnExist=False) == False and errorOnDuplicate:
			raise Exception("Event receiver already added")
	def getReceivers(self):
		return self._receivers

