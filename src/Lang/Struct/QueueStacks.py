class LIFOstack(object):
	"""Standard LIFO stack based on a list."""
	def __init__(self):
		self._list = []
	def push(self, item):
		self._list.append(item)
	def peek(self, index=1):
		return self._list[-index]
	
	def pop(self, *args, **kwargs):
		return self._list.pop(*args, **kwargs)
	def __getitem__(self, *args, **kwargs):
		return self._list.__getitem__(*args, **kwargs)
	def __setitem__(self, *args, **kwargs):
		return self._list.__setitem__(*args, **kwargs)
	def __len__(self, *args, **kwargs):
		return len(self._list)
	
	def __eq__(self, other):
		if isinstance(other, LIFOstack):
			return self._list == other._list
		return False
	def __ne__(self, other):
		return not (self == other)
	
	def __str__(self, *args, **kwargs):
		return self._list.__str__(*args, **kwargs)
	def __repr__(self, *args, **kwargs):
		return self._list.__repr__(*args, **kwargs)
