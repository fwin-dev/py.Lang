class LIFOstack(object):
	"""Standard LIFO stack based on a list."""
	def __init__(self):
		self._list = []
	def push(self, item):
		self._list.append(item)
	def peek(self, index=1):
		return self._list[-index]
	def __getattr__(self, funcName):
		if funcName in ("pop", "__getitem__", "__setitem__", "__len__", "__str__", "__repr__"):
			return getattr(self._list, funcName)
