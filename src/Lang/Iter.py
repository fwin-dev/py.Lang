from itertools import chain, islice

class PeekableIterable(object):
	def __init__(self, iterable):
		self._iterable = iterable
	
	def __iter__(self):
		return _PeekableIterator(self._iterable)
	
	def __getattr__(self, name):
		return getattr(self._iterable, name)

class _PeekableIterator:
	def __init__(self, iterable):
		self._iterator = iter(iterable)
	
	def next(self):
		return next(self._iterator)
	
	def hasNext(self):
		try:
			self.peek()
		except IndexError:
			return False
		return True
	
	def peek(self, numAhead=1):
		cutElems = tuple(islice(self._iterator, numAhead))
		self._iterator = chain(cutElems, self._iterator)
		return cutElems[-1]
