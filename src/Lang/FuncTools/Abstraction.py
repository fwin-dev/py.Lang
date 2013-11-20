def abstractmethod(method):
	"""
	This implementation of @abstractmethod only to be used with @classmethod to make an abstract class method
	because of bug: http://bugs.python.org/issue5867
	"""
	def default_abstract_method(*args, **kwargs):
		raise NotImplementedError("Abstract method " + repr(method) + " not implemented")
	default_abstract_method.__name__ = method.__name__
	return default_abstract_method

class FuncDesc:
	LOCAL = 2
	REMOTE = 3

class ArgDesc:
	SINGLE = 0
	MULTI = 1

class Descriptor:
	@classmethod
	@abstractmethod
	def isLocal(cls, funcName):
		pass
	@classmethod
	@abstractmethod
	def getArgTypes(cls, funcName):
		pass
	@classmethod
	@abstractmethod
	def getBuiltinFunction(cls, funcName, asStr=False):
		pass
