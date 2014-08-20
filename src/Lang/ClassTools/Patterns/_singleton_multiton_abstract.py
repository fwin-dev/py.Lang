from Lang.Struct import OrderedSet

class _Meta_SingletonMultitonAbstract(type):
	def getAllClasses(cls):
		return OrderedSet(class_ for class_ in cls._instances.iterkeys() if issubclass(class_, cls))
	def getAllInstances(cls):
		return dict((class_, instance) for class_, instance in cls._instances.iteritems() if issubclass(class_, cls))

class DuplicateInstanceException(Exception):
	pass
