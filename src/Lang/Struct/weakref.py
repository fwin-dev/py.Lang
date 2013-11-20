from weakref import *

try:
	WeakSet
except NameError:
	from weakrefset import WeakSet
