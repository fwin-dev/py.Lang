from _singleton_multiton_abstract import _Meta_SingletonMultitonAbstract, DuplicateInstanceException

class _Singleton_Abstract(_Meta_SingletonMultitonAbstract):
	_instances = {}
	def __getattribute__(cls, name):
		"""
		Intercept calls intended for bound methods on the instance, instead of unbound methods on the class.
		@see:	http://stackoverflow.com/questions/53225/how-do-you-check-whether-a-python-method-is-bound-or-not
		@see:	http://bugs.python.org/issue16851#msg181937
		"""
		obj = super(_Singleton_Abstract, cls).__getattribute__(name)
		if hasattr(obj, "__self__") and obj.__self__ == None:		# inspect.ismethod and inspect.isfunction are a little broken in py 2.7 - use this way of detecting methods vs. functions instead
			# then it's a method that expects self as first argument
			if cls in cls.getAllInstances():
				instance = cls.getAllInstances()[cls]
			else:
				instance = cls()	# try to create the instance by using __call__
			return getattr(instance, name)
		return obj

class _Meta_Singleton_OnDupRaiseException(_Singleton_Abstract):
	def __call__(cls, *args, **kwargs):
		if cls in cls._instances.iterkeys():
			raise DuplicateInstanceException("This class is a singleton, but you tried to create more than one instance")
		newInstance = super(_Meta_Singleton_OnDupRaiseException, cls).__call__(*args, **kwargs)
		cls._instances[cls] = newInstance
		return newInstance

class _Meta_Singleton_OnDupReturnExisting(_Singleton_Abstract):
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			newInstance = super(_Meta_Singleton_OnDupReturnExisting, cls).__call__(*args, **kwargs)
			cls._instances[cls] = newInstance
		return cls._instances[cls]

class Singleton_OnDupRaiseException(object):
	"""
	A singleton allows only one instance per class. Upon trying to create a second instance of a class, an exception is raised.
	
	This class should be the first in your MRO heirarchy in order to have a singleton. Any method calls
	(including `__init__`) will be applied to only one instance of the class.
	
	This class (actually the metaclass behind it) also maintains a dictionary of all created classes and the associated instance,
	thereby also providing a "class registration" mechanism. To see which classes have been registered:
	
		class Foo(Singleton_OnDupRaiseException):
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
	__metaclass__ = _Meta_Singleton_OnDupRaiseException

class Singleton_OnDupReturnExisting(object):
	"""
	A singleton allows only one instance per class. Upon trying to create a second instance of a class, the existing instance is returned.
	
	This class should be the first in your MRO heirarchy in order to have a singleton. Any method calls
	(including `__init__`) will be applied to only one instance of the class.
	
	This class (actually the metaclass behind it) also maintains a dictionary of all created classes and the associated instance,
	thereby also providing a "class registration" mechanism. To see which classes have been registered:
	
		class Foo(Singleton_OnDupReturnExisting):
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
	__metaclass__ = _Meta_Singleton_OnDupReturnExisting
