# works in Python 2 and 3

from _singleton_multiton_abstract import _SingletonMultitonAbstract, DuplicateInstanceException

import weakref

class _Singleton_Abstract(_SingletonMultitonAbstract):
	_instances = weakref.WeakValueDictionary()

class _Singleton_OnDupRaiseException(_Singleton_Abstract):
	def __call__(cls, *args, **kwargs):
		if cls in cls._instances.iterkeys():
			raise DuplicateInstanceException("This class is a singleton, but you tried to create more than one instance")
		newInstance = super(_Singleton_OnDupRaiseException, cls).__call__(*args, **kwargs)
		cls._instances[cls] = newInstance
		return newInstance

class _Singleton_OnDupReturnExisting(_Singleton_Abstract):
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			newInstance = super(_Singleton_OnDupReturnExisting, cls).__call__(*args, **kwargs)
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
	__metaclass__ = _Singleton_OnDupRaiseException

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
	__metaclass__ = _Singleton_OnDupReturnExisting
