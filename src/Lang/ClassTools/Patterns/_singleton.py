# works in Python 2 and 3

class _Singleton(type):
	_instances = {}
	
	def __call__(cls, *args, **kwargs):
		if cls in cls._instances:
			raise Exception("This class is a singleton, but you tried to create more than one instance")
		cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]
	def getAllClasses(cls):
		return [class_ for class_ in cls._instances.iterkeys() if issubclass(class_, cls)]
	def getAllInstances(cls):
		return dict((class_, instance) for class_, instance in cls._instances.iteritems() if issubclass(class_, cls))

class Singleton(_Singleton('SingletonMeta', (object,), {})):
	"""
	This class should be the first in your MRO heirarchy in order to have a singleton. Any method calls
	(including `__init__`) will be applied to only one instance of the class.
	
	This class (actually the metaclass behind it) also maintains a dictionary of all created classes (not instances),
	thereby providing a "class registration" mechanism. To see which classes have been registered:
	
	class Foo(Singleton):
		def __init__(self):
			super(Foo, self).__init__()
			...
	Foo()
	Foo.getAllClasses()
	# [<class '__main__.Foo'>]
	Foo.getAllInstances()
	# {<class '__main__.Foo'>: <__main__.Foo object at 0x1062a9210>}
	
	http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
	http://stackoverflow.com/questions/392160/what-are-your-concrete-use-cases-for-metaclasses-in-python
	"""
	pass
