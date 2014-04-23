from Lang.ClassTools import vars

from difflib import SequenceMatcher as _SequenceMatcher, SequenceMatcher
from collections import Hashable, Iterable, Sized
from itertools import izip

class SequenceMatcher(_SequenceMatcher, object):
	"""
	Improved difflib.SequenceMatcher.
	
	Can return non-matching blocks of objects, in addition to matching blocks of objects. It also provides an easier interface.
	
	Examples:
	
		diff = SequenceMatcher(tuple("aebcdef"), tuple("abbcdgef"))
		print(list(diff.get_matching_blocks()))
		print(list(diff.get_mismatching_blocks()))
		print(list(diff.get_matching_elems()))
		print(list(diff.get_mismatching_elems()))
		
		Prints the following:
		
		[BlockMatch(a={index=0,size=1}, b={index=0,size=1}), BlockMatch(a={index=2,size=3}, b={index=2,size=3}), BlockMatch(a={index=5,size=2}, b={index=6,size=2})]
		[BlockMismatch(a={index=1,size=1}, b={index=1,size=1}), BlockMismatch(a=None, b={index=5,size=1})]
		[ElemMatch(a=('a',), b=('a',)), ElemMatch(a=('b', 'c', 'd'), b=('b', 'c', 'd')), ElemMatch(a=('e', 'f'), b=('e', 'f'))]
		[ElemMismatch(a=('e',), b=('b',)), ElemMismatch(a=None, b=('g',))]
	"""
	def __init__(self, *args, **kwargs):
		"""
		@param *args:	2 arguments that specify the 2 things to compare should be passed in here.
		"""
		assert len(args) in (0,2)
		if len(args) == 2:
			kwargs["a"] = args[0]
			kwargs["b"] = args[1]
		assert "a" in kwargs and "b" in kwargs
		kwargs["a"] = self._checkType(kwargs["a"])
		kwargs["b"] = self._checkType(kwargs["b"])
		super(SequenceMatcher, self).__init__(**kwargs)
	@classmethod
	def _checkType(cls, side):
		assert isinstance(side, Iterable)
		if not isinstance(side, Sized):		# object must be len-able and subscriptable to be used in diff
			side = tuple(side)
		containerInstance = side[0]
		if not isinstance(containerInstance, Hashable):
			raise Exception("Elements in iterable must be hashable. Ex. use FrozenDict instead of dict, frozenset instead of set, etc.")		
		return side
	
	def __eq__(self, other):
		return isinstance(other, _SequenceMatcher) and self.a == other.a and self.b == other.b
	def __ne__(self, other):
		return not (self == other)
	
	def ratio(self):
		"""
		Corrects ratio in difflib.SequenceMatcher
		
		Before, the ratio function would add the length of `a` and `b` in its formula, but usually the user wants to
		consider the difference of only one side.
		"""
		superRatio = super(SequenceMatcher, self).ratio()
		return superRatio + ((1 - superRatio) / 2)
	
	def get_matching_blocks(self):
		# avoid a bug where subsequent calls to this function return a regular tuple instead of a named tuple
		for block in super(SequenceMatcher, self).get_matching_blocks():
			block = _BlockMatch(*block)
			if block.size != 0:
				yield block
	
	def _diffSingleSide(self, currentBlock, lastBlock, sideName):
		diffStart = getattr(lastBlock, sideName).index + lastBlock.size
		diffLen = getattr(currentBlock, sideName).index - diffStart
		if diffLen == 0:
			return None
		return _BlockSide(diffStart, diffLen)
	def get_mismatching_blocks(self):
		lastMatch = None
		for currentMatch in self.get_matching_blocks():
			if lastMatch != None and currentMatch.size != 0:
				yield _BlockMismatch(self._diffSingleSide(currentMatch, lastMatch, "a"),
									 self._diffSingleSide(currentMatch, lastMatch, "b"))
			lastMatch = currentMatch
	
	@classmethod
	def _advanceIter(cls, iterator, currentIndex, wantedStartIndex, length):
		nextValue = iterator.next()
		while currentIndex != wantedStartIndex:
			nextValue = iterator.next()
			currentIndex += 1
		yield nextValue
		for _ in range(0, length-1):
			nextValue = iterator.next()
			yield nextValue
	@classmethod
	def _blocksToElems(cls, blocks, originalElems, sideName):
		iterator = iter(originalElems)
		currentIndex = 0
		for block in blocks:
			side = getattr(block, sideName)
			if side == None:
				yield _ElemsBlockSide(block, None)
				continue
			elems = cls._advanceIter(iterator, currentIndex, side.index, side.size)
			yield _ElemsBlockSide(block, elems)
			currentIndex = side.index + side.size
	
	def _getElems(self, getBlocksFunc):
		blockElemsPairsA = self._blocksToElems(getBlocksFunc(), self.a, "a")
		blockElemsPairsB = self._blocksToElems(getBlocksFunc(), self.b, "b")
		return izip(blockElemsPairsA, blockElemsPairsB)
	
	def get_matching_elems(self):
		"""
		Tuples and lists are used here instead of generators.
		"""
		allElems = []
		for elemMatch in self.get_matching_elems_useOnce():
			elemMatch._convertGensToIndexable()
			allElems.append(elemMatch)
		return allElems
	def get_matching_elems_useOnce(self):
		"""
		Generators will be returned which can only be iterated over once. Generators are faster only if some elements are wanted.
		"""
		for blockElemsPairA, blockElemsPairB in self._getElems(self.get_matching_blocks):
			yield _ElemMatch(blockElemsPairA.elems, blockElemsPairB.elems)
	def get_mismatching_elems(self):
		"""
		Tuples and lists are used here instead of generators.
		"""
		allElems = []
		for elemMatch in self.get_mismatching_elems_useOnce():
			elemMatch._convertGensToIndexable()
			allElems.append(elemMatch)
		return allElems
	def get_mismatching_elems_useOnce(self):
		"""
		Generators will be returned which can only be iterated over once. Generators are faster only if some elements are wanted.
		"""
		for blockElemsPairA, blockElemsPairB in self._getElems(self.get_mismatching_blocks):
			yield _ElemMismatch(blockElemsPairA.elems, blockElemsPairB.elems)
	
	def get_matching(self):
		for blockElemsPairA, blockElemsPairB in self._getElems(self.get_matching_blocks):
			yield _ElemBlockMatch(blockElemsPairA, blockElemsPairB)
	def get_mismatching(self):
		for blockElemsPairA, blockElemsPairB in self._getElems(self.get_mismatching_blocks):
			yield _ElemBlockMismatch(blockElemsPairA, blockElemsPairB)


class _BlockSide(object):
	__slots__ = ("index", "size")
	def __init__(self, index, size):
		self.index = index
		self.size = size
	def __str__(self):
		return "{index=" + str(self.index) + ",size=" + str(self.size) + "}"
	def __repr__(self):
		return str(self)
class _ElemsBlockSide(object):
	"""
	`elems` attribute is guaranteed to be an iterable, not indexable
	@see _BlockSide
	"""
	__slots__ = ("block", "elems")
	def __init__(self, block, elems):
		self.block = block
		self.elems = elems
	def __getattr__(self, name):
		return getattr(self.block, name)
	def __str__(self):
		return "{block=" + str(self.block) + ",elems=" + str(self.elems) + "}"
	def __repr__(self):
		return str(self)

class _TwoSide(object):
	__slots__ = ("a", "b")
	def __init__(self, a, b):
		self.a = a
		self.b = b
	def __str__(self):
		attrs = ", ".join((key + "=" + str(getattr(self, key)) for key in vars(self.__class__)))
		return self.__class__.__name__.strip("_") + "(" + attrs + ")"
	def __repr__(self):
		return str(self)
	def _convertGensToIndexable(self):
		self.a = tuple(self.a) if self.a != None else None
		self.b = tuple(self.b) if self.b != None else None

class _Block(_TwoSide):
	pass
class _BlockMatch(_Block):
	def __init__(self, indexA, indexB, size):
		_TwoSide.__init__(self, _BlockSide(indexA, size), _BlockSide(indexB, size))
	def __getattr__(self, name):
		if name == "size":
			return self.a.size
		raise AttributeError
	def __getitem__(self, index):	# emulates tuple access for backwards compatibility in difflib
		return (self.a.index, self.b.index, self.a.size)[index]
class _BlockMismatch(_Block):
	def __init__(self, blockSideA, blockSideB):
		_TwoSide.__init__(self, blockSideA, blockSideB)

class _ElemMatch(_TwoSide):
	pass
class _ElemMismatch(_TwoSide):
	pass
class _ElemBlockMatch(_TwoSide):
	pass
class _ElemBlockMismatch(_TwoSide):
	pass

