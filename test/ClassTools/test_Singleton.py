from test_SingletonMultitonAbstract import _Test_SingletonMultiton_Abstract
from Lang.ClassTools.Patterns import Singleton_OnDupRaiseException, Singleton_OnDupReturnExisting, DuplicateInstanceException
import unittest

class _Test_Singleton_Abstract(_Test_SingletonMultiton_Abstract):
	pass

class Test_Singleton_OnDupRaiseException(_Test_Singleton_Abstract, unittest.TestCase):
	def getSuperClass(self):
		return Singleton_OnDupRaiseException
	
	def test_multipleInstances_raiseException(self):
		class Foo(self.getSuperClass()):
			def __init__(self, value):
				super(Foo, self).__init__()
				self.value = value
		class Bar(Foo):
			pass
		a = Bar(3)	# hold a reference here
		self.assertRaises(DuplicateInstanceException, lambda: Bar(4))

class Test_Singleton_OnDupReturnExisting(_Test_Singleton_Abstract, unittest.TestCase):
	def getSuperClass(self):
		return Singleton_OnDupReturnExisting

	def test_multipleInstances_alwaysOriginalInstance(self):
		class Foo(self.getSuperClass()):
			def __init__(self, value):
				super(Foo, self).__init__()
				self.value = value
			def __eq__(self, other):
				return isinstance(other, self.__class__) and self.value == other.value
			def __ne__(self, other):
				return not self.__eq__(other)
		class Bar(Foo):
			pass
		a = Bar(3)	# hold a reference here
		b = Bar(4)
		self.assertEquals(a, b)
