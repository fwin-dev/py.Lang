# Taken from http://code.activestate.com/recipes/576696/ (r5)
# Modified by Jesse Cowles

import collections
from weakref import proxy

class Link(object):
	__slots__ = 'prev', 'next', 'key', '__weakref__'
	def __init__(self, key=None):
		self.key = key

class OrderedSet(collections.MutableSet):
	"""
	A set that remembers the order elements were added.
	Functions in `collections.MutableSet` are supported, such as `|=` (union/`__ior__`), etc.
	*** NOTE THAT SLICE NOTATION IS STILL BEING IMPLEMENTED ***
	
	The internal self.__map dictionary maps keys to links in a doubly linked list.
	The circular doubly linked list starts and ends with a sentinel element.
	The sentinel element never gets deleted (this simplifies the algorithm).
	The prev/next links are weakref proxies (to prevent circular references). Individual links are kept alive by
	the hard reference in self.__map. Those hard references disappear when a key is deleted from an OrderedSet.
	"""
	
	def __init__(self, iterable=None):
		self.__root = root = Link()		 # sentinel node for doubly linked list
		root.prev = root.next = root
		self.__map = {}					 # key --> link
		if iterable is not None:
			self |= iterable
	
	def __setitem__(self, indexOrSlice, value):
		if isinstance(indexOrSlice, slice):
			raise NotImplementedError
		else:	# replace mode with single - same as python standard library
			return self._replace(self._getLink_byIndex(indexOrSlice), value)
	
	def __delitem__(self, index):
		return self.discard(self[index])
	
	def _replace(self, link, newElem):
		self._insertBefore_link(newElem, link, updateOnExist=True)
		self.discard(link.key)
	def replace(self, oldElem, newElem):
		if oldElem not in self.__map:
			raise ValueError(str(oldElem) + " is not in OrderedList")
		self._replace(self.__map[oldElem], newElem)
	
	def __getitem__(self, indexOrSlice):
		if isinstance(indexOrSlice, slice):
			return OrderedSet(link.key for link in self._iterLinks(indexOrSlice))
		else:
			return self._getLink_byIndex(indexOrSlice).key
	def index(self, elem):
		if elem not in self.__map:
			raise ValueError(str(elem) + " is not in OrderedList")
		for i, link_key in enumerate(self):
			if elem == link_key:
				return i
	
	def _iterLinks(self, slice_):
		if isinstance(slice_, slice):
			if slice_.start == slice_.stop == 0:
				raise StopIteration()
			slice_ = self._convertSlice(slice_)
			nextLink = self._getLink_byIndex(slice_.start)
			betweenStep = 0		# if betweenStep, don't yield; 0 == False, > 0 == True
			iterAll_step = max(1, min(-1, slice_.step))	#   = -1 if negative step, +1 if positive step
			iterAll_stop = slice_.stop - slice_.start + iterAll_step		# + iterAll_step because range stops 1 short of last number
			for _ in range(0, iterAll_stop, iterAll_step):
				if betweenStep == 0:
					yield nextLink
				betweenStep %= abs(slice_.step)
				if slice_.step > 0:	nextLink = nextLink.next
				else:				nextLink = nextLink.prev
		else:
			raise TypeError("Incorrect index type for OrderedSet")
	
	def _convertSlice(self, slice_):
		"""
		Does 2 things:
		- Converts slice indices from negative to positive.
		- Converts from standard slice indices (as used in other python data types, where indices are
		representative of the gaps between elements) to indices that correspond to elements.
		"""
		return slice(self._getPositiveIndex(slice_.start) if slice_.start != None else 0,
					 self._getPositiveIndex(self._getPositiveIndex(slice_.stop, checkLen=False) - 1),
					 slice_.step if slice_.step != None else 1)
	
	def _getPositiveIndex(self, index, checkLen=True):
		if not isinstance(index, int):
			raise TypeError("Incorrect index type for OrderedSet")
		if index < 0:
			index = len(self) + index	# convert to positive index
		if checkLen and (index >= len(self) or index < 0):
			raise KeyError("Index out of range")
		return index
	
	def _getLink_byIndex(self, index):
		index = self._getPositiveIndex(index)
		root = self.__root
		if abs(index) < len(self) / 2:	# faster to iterate in forward order
			curr = root.next
			for i in range(0, index + 1):
				if i == index:
					return curr
				curr = curr.next
		else:							# faster to iterate in reverse order
			curr = root.prev
			index = len(self) - index - 1	# calculates positive index when iterating over set in reverse
			for i in range(0, index + 1):
				if i == index:
					return curr
				curr = curr.prev
	
	def insertAt(self, index, newElem, updateOnExist=True):
		if index < len(self):
			return self.insertBefore(newElem, self[index], updateOnExist=updateOnExist)
		else:
			return self.add(newElem, updateOnExist=updateOnExist)
		
	def insertBefore(self, newElemBefore, oldElemAfter, updateOnExist):
		"""See _insertBefore_link(...) method."""
		return self._insertBefore_link(newElemBefore, self.__map[oldElemAfter], updateOnExist)
	
	def insertMultiBefore(self, newElemsBefore, oldElemAfter, updateOnExist):
		if oldElemAfter not in self.__map:
			raise ValueError("oldElemAfter not in OrderedSet")
		return self._insertBefore_links(newElemsBefore, self.__map[oldElemAfter], updateOnExist)
	
	def _insertBefore_link(self, newElemBefore, oldLinkAfter, updateOnExist):
		"""
		Inserts newElemBefore into the current position of oldLinkAfter. oldLinkAfter will then come after newElemBefore.
		
		oldLinkAfter	--- Must be an existing link in the map.
		newElemBefore	--- New element to insert.
		updateOnExist	--- If True and newElemBefore is already in the list, the already existing newElemBefore will be
							removed and the newElemBefore passed into this function will be inserted before oldLinkAfter.
							If False and newElemBefore is already in the list, newElemBefore will not be inserted, and
							the whole list will not be modified.
		
		Returns True if link was inserted, False if not inserted because it already exists and updateOnExist is False.
		"""
		if oldLinkAfter != self.__root and oldLinkAfter.key not in self.__map:
			raise ValueError(str(oldLinkAfter.key) + " is not in OrderedSet")
		if newElemBefore in self.__map:
			if updateOnExist:
				self.discard(newElemBefore)
			else:
				return False
		
		self.__map[newElemBefore] = link = Link(newElemBefore)
		link.prev, link.next = oldLinkAfter.prev, oldLinkAfter
		link.prev.next = oldLinkAfter.prev = proxy(link)
		return True
	
	def _insertBefore_links(self, newElemsBefore, oldLinkAfter, updateOnExist):
		"""
		Returns True if all links were inserted, False otherwise.
		"""
		allInserted = True
		for newElemBefore in reversed(newElemsBefore):
			wasInserted = self._insertBefore_link(newElemBefore, oldLinkAfter, updateOnExist)
			allInserted = allInserted and wasInserted
			if wasInserted:
				oldLinkAfter = self.__map[newElemBefore]
		return allInserted
	
	def add(self, elem, updateOnExist=False):
		"""Same as `append`"""
		return self._insertBefore_link(elem, self.__root, updateOnExist=updateOnExist)
	
	def append(self, elem, updateOnExist=False):
		"""
		If elem is not in the OrderedSet, append elem to the OrderedSet. Same as `add`.
		
		@param updateOnExist	bool:	If elem is already in the OrderedSet and this is `False`, do nothing. If this is `True`, the old element is removed and the new one is appended.
		
		@return bool: `True` if new elem was inserted, `False` if not inserted because it already exists and `updateOnExist` is `False`.
		"""
		return self._insertBefore_link(elem, self.__root, updateOnExist=updateOnExist)
	
	def discard(self, elem):
		if elem in self.__map:		
			link = self.__map.pop(elem)
			link.prev.next = link.next
			link.next.prev = link.prev
	
	def pop(self):
		if len(self) == 0:
			raise KeyError("set is empty")
		elem = next(reversed(self)) if len(self) > 1 else next(iter(self))
		self.discard(elem)
		return elem
	
	def __contains__(self, elem):
		return elem in self.__map
	
	def __iter__(self):
		"""Traverse the linked list in order."""
		for link in self._iterLinks(slice(0, len(self))):
			yield link.key
	
	def __reversed__(self):
		"""Traverse the linked list in reverse order."""
		for link in self._iterLinks(slice(len(self)-1, 0, -1)):
			yield link.key
	
	def __repr__(self):
		"""
		Same format as OrderedDict.
		For the empty set, it returns: `OrderedSet()`
		Otherwise, it returns the values inside square brackets: `OrderedSet(["a", "b", "c"])`
		"""
		if len(self) == 0:
			return self.__class__.__name__ + "()"
		return self.__class__.__name__ + "(" + str(list(self)) + ")"

	def __len__(self):
		return len(self.__map)
	
	def __eq__(self, other):
		if isinstance(other, OrderedSet):
			return len(self) == len(other) and list(self) == list(other)
		return not self.isdisjoint(other)
