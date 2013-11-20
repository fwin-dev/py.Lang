from Lang.Struct import OrderedSet
import weakref

class RegisteredInstances(object):
	"""
	Maintains a record of every created instance of a class. Don't forget to call `super(...).__init__(...)`.
	
	http://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined/5189271
	
	Examples:
	https://github.com/ask/celery/blob/6b91c7e0f2d9d1c1f16899161977ae0c2662f9fd/celery/task/base.py
	https://github.com/ask/celery/blob/6b91c7e0f2d9d1c1f16899161977ae0c2662f9fd/celery/registry.py
	"""
	
	_allInstances_weakrefs = []
	
	def __init__(self):
		if self not in reversed(self.getAllInstances()):
			self._allInstances_weakrefs.append(weakref.ref(self, self.__removeInstance))
	
	@classmethod
	def __removeInstance(cls, instance_weakref):
		cls._allInstances_weakrefs.remove(instance_weakref)
	
	@classmethod
	def getAllClasses(cls):
		return OrderedSet(instance.__class__ for instance in cls.__filter_sameClassAsSelf())
	@classmethod
	def getAllInstances(cls):
		return list(cls.__filter_sameClassAsSelf())
	
	@classmethod
	def __filter_sameClassAsSelf(cls):
		return (instance_weakref() for instance_weakref in cls._allInstances_weakrefs if isinstance(instance_weakref(), cls))
