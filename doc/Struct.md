# <a name="struct"></a>Struct

Various structures for holding data.

## LIFO/Stack

Python lists can be used as stacks, but they don't have the normal API that a stack does.

	from Lang.Struct import LIFOstack
	stack = LIFOstack()
	stack.push("a")
	element = stack.peek()
	element = stack.pop()

## Frozen dictionary

In the case where a hashable dictionary is needed, `FrozenDict` can be used. `FrozenDict` is just like a normal `dict`
except it cannot be modified.

	from Lang.Struct import FrozenDict
	dict_ = FrozenDict({"asdf": 1, "jkl": 2})

## Ordered set

The built-in python `set` is just like a `list`, except for 2 things:

* Sets can't contain duplicate elements
* Sets are unordered
 
However, there are some cases where an ordered set (aka a list with no duplicate elements) is desirable. For this, use
the `OrderedSet` provided here, which provides a similar implementation compared to the built-in `set`, but also provides
methods typically found in a list, such as `insert`/`insertAt`. Refer to the source and unit test for a list of all methods.

	from Lang.Struct import OrderedSet
	set_ = OrderedSet(range(1,10))
