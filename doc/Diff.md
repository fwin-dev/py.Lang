# <a name="diff"></a>Diff

This differ builds upon `difflib.SequenceMatcher` which can diff any python objects with `__eq__` implemented, contained
within a list, tuple, etc. However, the built in class only provides methods for getting matching sets of indices which
refer to matching elements, leaving you to infer which indices don't match. It also doens't give you direct access to
elements that do or don't match. This differ adds all of that functionality. It also fixes:

* A bug: In the built in differ, subsequent calls to `get_matching_blocks()` will return results in a different format due to caching
* Calculating the similarity ratio: The built in differ calculates this ratio taking both diff sides into account, but what's usually wanted is how much one side is similar/different compared to the other side: `(1 - ratio) / 2 + ratio`

Examples:

	from Lang.Diff import SequenceMatcher
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

More functions are available, including:

* `getmatching()` and `getmismatching()`
  * These return structures with `.block` and `.elems` attributes containing both block indices and the elems which the block refers to
* `get_matching_elems_useOnce()` and `get_mismatching_elems_useOnce()`
  * These are the same as `get_matching_elems()` and `get_mismatching_elems()` except that they are generators instead of functions returning a list
