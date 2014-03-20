def abstractmethod(method):
	"""
	This implementation of @abstractmethod only to be used with @classmethod to make an abstract class method
	because of bug: http://bugs.python.org/issue5867
	"""
	def default_abstract_method(*args, **kwargs):
		raise NotImplementedError("Abstract method " + repr(method) + " not implemented")
	default_abstract_method.__name__ = method.__name__
	return default_abstract_method
