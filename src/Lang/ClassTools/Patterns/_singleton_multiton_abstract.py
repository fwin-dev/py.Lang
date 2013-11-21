class _SingletonMultitonAbstract(type):
	def getAllClasses(cls):
		return [class_ for class_ in cls._instances.iterkeys() if issubclass(class_, cls)]
	def getAllInstances(cls):
		return dict((class_, instance) for class_, instance in cls._instances.iteritems() if issubclass(class_, cls))
