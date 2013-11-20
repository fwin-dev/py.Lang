from _OrderedSet import OrderedSet
from _FrozenDict import FrozenDict
from QueueStacks import LIFOstack

try:
	from collections import OrderedDict
except ImportError:
	from ordereddict import OrderedDict
