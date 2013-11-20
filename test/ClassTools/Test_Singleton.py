from Lang.ClassTools.Patterns import Singleton
import unittest

class Test_Singleton(unittest.TestCase):
	def test_noMultipleInstances(self):
		
		class Foo(Singleton):
			def __init__(self, value):
				super(Foo, self).__init__()
				self.value = value
		class Bar(Foo):
			pass
		a = Bar(3)	# hold a reference here
		self.assertRaises(Exception, lambda: Bar(4))
	
	def test_basic(self):
		
		class Foo(Singleton):
			def __init__(self, value):
				self.value = value
		a = Foo(3)
		self.assertEqual(len(Foo.getAllInstances()), 1)
	
	def test_inheritance_getAllInstances_getAllClasses(self):
		
		class Foo(Singleton):
			def __init__(self, value):
				super(Foo, self).__init__()
				self.value = value
		class Bar(Foo):
			pass
		
		a = Foo(3)
		b = Bar(4)
		self.assertEqual(a.value, 3)
		self.assertEqual(b.value, 4)
		self.assertEqual(len(Foo.getAllClasses()), 2)
		self.assertEqual(len(Foo.getAllInstances()), 2)
		self.assertEqual(len(Bar.getAllClasses()), 1)
		self.assertEqual(len(Bar.getAllInstances()), 1)
	
	def test_unrelated(self):
		
		class Foo(Singleton):
			def __init__(self, value):
				super(Foo, self).__init__()
				self.value = value
		class Bar(Singleton):
			def __init__(self):
				super(Bar, self).__init__()
		
		a = Foo(2)
		b = Bar()
		
		self.assertEqual(len(Foo.getAllClasses()), 1)
		self.assertEqual(len(Foo.getAllInstances()), 1)
		self.assertEqual(len(Bar.getAllClasses()), 1)
		self.assertEqual(len(Bar.getAllInstances()), 1)
