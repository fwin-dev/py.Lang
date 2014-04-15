import copy

class FrozenDict(dict):
	"""
	An immutable, hashable dictionary.
	
	Based on:
	http://code.activestate.com/recipes/414283/
	"""
	@classmethod
	def _blocked_attribute(cls, obj):
		raise AttributeError("A FrozenDict cannot be modified.")
	_blocked_attribute = property(_blocked_attribute)
	
	__delitem__ = __setitem__ = clear = _blocked_attribute
	pop = popitem = setdefault = update = _blocked_attribute
	
	def __new__(cls, *args, **kw):
		new = dict.__new__(cls)
		
		args_ = []
		for arg in args:
			if isinstance(arg, dict):
				arg = copy.copy(arg)
				for k, v in arg.items():
					if isinstance(v, dict):
						arg[k] = FrozenDict(v)
					elif isinstance(v, list):
						v_ = list()
						for elm in v:
							if isinstance(elm, dict):
								v_.append(FrozenDict(elm))
							else:
								v_.append(elm)
						arg[k] = tuple(v_)
				args_.append(arg)
			else:
				args_.append(arg)
		
		dict.__init__(new, *args_, **kw)
		return new
	
	def __init__(self, *args, **kw):
		pass
	
	def __hash__(self):
		try:
			return self._cached_hash
		except AttributeError:
			self._cached_hash = hash(frozenset(self.items()))
			return self._cached_hash
	
	def __repr__(self):
		return self.__class__.__name__ + "(" + dict.__repr__(self) + ")"

