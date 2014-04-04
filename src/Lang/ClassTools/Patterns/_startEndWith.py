from abc import ABCMeta, abstractmethod

class StartEndWith(object):
	"""Automatic `with` statement support, once `_start` and `_end` are overridden/implemented."""
	__metaclass__ = ABCMeta
	
	def __init__(self, allowStartWhileRunning=False, useOnce=False,
				methodName_start="start", methodName_end="end", methodName_isActive="isActive", *args, **kwargs):
		super(StartEndWith, self).__init__(*args, **kwargs)
		
		self._allowStartWhileRunning = allowStartWhileRunning
		self._useOnce = useOnce
		self._ranOnce = False
		self.__isActive = False
		
		self._methodName_start = methodName_start
		self._methodName_end = methodName_end
		self._methodName_isActive = methodName_isActive
		setattr(self, self._methodName_start, self._public_start)
		setattr(self, self._methodName_end, self._public_end)
		setattr(self, self._methodName_isActive, self.__method_isActive)
	
	def __enter__(self):
		self._common_start()
		return self
	def __exit__(self, *args, **kwargs):
		self._common_end()
		return False
	
	def __method_isActive(self):
		return self.__isActive
	def _public_start(self, *args, **kwargs):
		return self._common_start(*args, **kwargs)
	def _public_end(self, *args, **kwargs):
		return self._common_end(*args, **kwargs)
	
	def _common_start(self, *args, **kwargs):
		if self.__isActive:
			if not self._allowStartWhileRunning:
				raise Exception(self.__class__.__name__ + " instance already " + self._methodName_start + ("ed" if self._methodName_start[-1] != "e" else "d"))
			else:
				return
		if self._useOnce and self._ranOnce == True:
			raise Exception("Tried to re-" + self._methodName_start + " " + self.__class__.__name__ + " instance, which is not allowed. Create a new instance instead, if needed.")
		self.__isActive = True
		return self._start(*args, **kwargs)
	
	def _common_end(self, *args, **kwargs):
		if not self.__isActive:
			raise Exception(self.__class__.__name__ + " instance not yet started, so cannot " + self._methodName_end + " it")
		result = self._end(*args, **kwargs)
		self.__isActive = False
		self._ranOnce = True
		return result
	
	@abstractmethod
	def _start(self, *args, **kwargs):
		pass
	@abstractmethod
	def _end(self, *args, **kwargs):
		pass
