from Test_SingletonMultitonAbstract import _Test_SingletonMultiton_Abstract
from Lang.ClassTools.Patterns import Multiton_OneEquivalentInstance_OnDupRaiseException, Multiton_OneEquivalentInstance_OnDupReturnExisting
import unittest

class _Test_Multiton_OneEquivalentInstance_Abstract(_Test_SingletonMultiton_Abstract):
	pass

class Test_Multiton_OneEquivalentInstance_OnDupRaiseException(_Test_Multiton_OneEquivalentInstance_Abstract, unittest.TestCase):
	def getSuperClass(self):
		return Multiton_OneEquivalentInstance_OnDupRaiseException
	
	def test_equalityByMemoryAddress(self):
		class Foo(self.getSuperClass()):
			def __init__(self, value):
				super(Foo, self).__init__()
				self.value = value
		class Bar(Foo):
			pass
		a = Bar(3)
		b = Bar(3)
		self.assertNotEqual(id(a), id(b))
	
	def test_equalityBy__eq__(self):
		class Foo(self.getSuperClass()):
			def __init__(self, value):
				super(Foo, self).__init__()
				self.value = value
			def __eq__(self, other):
				return isinstance(other, self.__class__) and self.value == other.value
			def __str__(self):
				return repr(self) + ": " + str(self.value)
		class Bar(Foo):
			pass
		a = Bar(3)	# hold a reference here
		self.assertRaises(Exception, lambda: Bar(3))
