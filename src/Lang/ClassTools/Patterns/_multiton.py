from _singleton_multiton_abstract import _Meta_SingletonMultitonAbstract, DuplicateInstanceException

from Lang.Struct import weakref
from abc import ABCMeta, abstractmethod

class _Meta_Multiton_OneEquivalentInstance(_Meta_SingletonMultitonAbstract, ABCMeta):
	_instances = {}
	
	def getAllClasses(cls):
		cls._multiton_pruneClasses()
		return super(_Meta_Multiton_OneEquivalentInstance, cls).getAllClasses()
	def getAllInstances(cls):
		cls._multiton_pruneClasses()
		return super(_Meta_Multiton_OneEquivalentInstance, cls).getAllInstances()
	
	@abstractmethod
	def _multiton_onDup(self, existingInstance, newInstance):
		pass
	
	def _multiton_pruneClasses(cls):
		"""
		Since we don't know when exactly any instance references will disappear in a WeakSet (because it provides no callback
		registration method for when an instance is garbage collected), we have to manually check the size of the WeakSet here,
		and remove the set and class if it's 0.
		"""
		cls._instances = dict((class_, instanceSet) for class_, instanceSet in cls._instances.iteritems() if len(instanceSet) > 0)
	
	def __call__(cls, *args, **kwargs):
		newInstance = super(_Meta_Multiton_OneEquivalentInstance, cls).__call__(*args, **kwargs)		# create new, normal class instance
		if cls not in cls._instances:
			cls._instances[cls] = weakref.WeakSet()
		for instance in cls._instances[cls]:
			if instance == newInstance:
				return cls._multiton_onDup(instance, newInstance)
		cls._instances[cls].add(newInstance)
		return newInstance

class _Meta_Multiton_OneEquivalentInstance_OnDupRaiseException(_Meta_Multiton_OneEquivalentInstance):
	def _multiton_onDup(self, existingInstance, newInstance):
		raise DuplicateInstanceException("An equivalent instance has already been created")

class _Meta_Multiton_OneEquivalentInstance_OnDupReturnExisting(_Meta_Multiton_OneEquivalentInstance):
	def _multiton_onDup(self, existingInstance, newInstance):
		return existingInstance

class Multiton_OneEquivalentInstance_OnDupRaiseException(object):
	"""
	Only one instance of this class is allowed per equivalent instance. An equivalent instance is defined by using the `==` operator.
	This class should be the first in your MRO heirarchy in order to have a multiton with only one equivalent instance allowed.
	
	Because this multiton must use `==` (which can use `__eq__` in the class instance, for example), it must create the instance to do
	the comparison, which means there will actually be two instances for a short-lived time, while the comparison is being done.
	Because of this, since more than one equivalent instance is possible during `__init__` and `__eq__` calls, make sure that those
	methods do not rely upon there only being a single equivalent instance.
	
	If an equivalent instance already exists, an exception will be raised.
	
	Similar solutions and useful links:
	- http://lifegoo.pluskid.org/?p=345
	"""
	__metaclass__ = _Meta_Multiton_OneEquivalentInstance_OnDupRaiseException

class Multiton_OneEquivalentInstance_OnDupReturnExisting(object):
	"""
	Only one instance of this class is allowed per equivalent instance. An equivalent instance is defined by using the `==` operator.
	This class should be the first in your MRO heirarchy in order to have a multiton with only one equivalent instance allowed.
	
	Because this multiton must use `==` (which can use `__eq__` in the class instance, for example), it must create the instance to do
	the comparison, which means there will actually be two instances for a short-lived time, while the comparison is being done.
	Because of this, since more than one equivalent instance is possible during `__init__` and `__eq__` calls, make sure that those
	methods do not rely upon there only being a single equivalent instance.
	
	If an equivalent instance already exists, that instance will be returned instead of creating another one.
	
	Similar solutions and useful links:
	- http://lifegoo.pluskid.org/?p=345
	"""
	__metaclass__ = _Meta_Multiton_OneEquivalentInstance_OnDupReturnExisting
