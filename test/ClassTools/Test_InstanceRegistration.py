from Lang.ClassTools import RegisteredInstances
import unittest

class Test_InstanceRegistration(unittest.TestCase):
	def test_garbageCollection(self):
		
		class Foo(RegisteredInstances):
			def __init__(self, value):
				super(Foo, self).__init__()
				self.value = value
		Foo(3)
		# fell out of scope here
		
		self.assertEqual(len(Foo.getAllInstances()), 0, Foo.getAllInstances())
		self.assertEqual(len(Foo.getAllClasses()), 0, Foo.getAllClasses())
	
	def test_basic(self):
		
		class Foo(RegisteredInstances):
			def __init__(self, value):
				super(Foo, self).__init__()
				self.value = value
		a = Foo(3)
		b = Foo(4)
		
		self.assertEqual(len(Foo.getAllInstances()), 2, Foo.getAllInstances())
		self.assertEqual(Foo.getAllInstances()[0], a)
		self.assertEqual(Foo.getAllInstances()[1], b)
		
		self.assertEqual(len(Foo.getAllClasses()), 1, Foo.getAllClasses())
		self.assertEqual(Foo.getAllClasses()[0], Foo)
	
	def test_inheritance(self):
		
		class Foo(RegisteredInstances):
			def __init__(self, value):
				super(Foo, self).__init__()
				self.value = value
		class Bar(Foo):
			pass
		
		a = Bar(3)
		b = Foo(4)
		c = Bar(5)
		
		# test Foo
		self.assertEqual(len(Foo.getAllInstances()), 3, Foo.getAllInstances())
		self.assertEqual(Foo.getAllInstances()[0], a)
		self.assertEqual(Foo.getAllInstances()[1], b)
		self.assertEqual(Foo.getAllInstances()[2], c)
		
		self.assertEqual(len(Foo.getAllClasses()), 2)
		self.assertEqual(Foo.getAllClasses()[0], Bar)
		self.assertEqual(Foo.getAllClasses()[1], Foo)
		
		# test Bar
		self.assertEqual(len(Bar.getAllInstances()), 2, Foo.getAllInstances())
		self.assertEqual(Bar.getAllInstances()[0], a)
		self.assertEqual(Bar.getAllInstances()[1], c)
		
		self.assertEqual(len(Bar.getAllClasses()), 1)
		self.assertEqual(Bar.getAllClasses()[0], Bar)
