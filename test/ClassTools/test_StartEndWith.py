from Lang.ClassTools.Patterns import StartEndWith
import unittest

class Test_StartEndWith(unittest.TestCase):
	def newInstance(self, allowStartWhileRunning=False, useOnce=False):
		
		class Foo(StartEndWith):
			def __init__(self, **kwargs):
				super(Foo, self).__init__(**kwargs)
				self.hasStarted = False
			def _start(self, *args, **kwargs):
				self.hasStarted = True
			def _end(self, *args, **kwargs):
				self.hasStarted = False
		
		return Foo(allowStartWhileRunning=allowStartWhileRunning, useOnce=useOnce,
					methodName_start="start1", methodName_end="end1", methodName_isActive="isActive1")
	
	def test_basic_manualCall(self):
		a = self.newInstance()
		self.assertEqual(a.hasStarted, False)
		self.assertEqual(a.isActive1(), False)
		self.assertRaises(Exception, a.end1)
		
		a.start1()
		self.assertEqual(a.hasStarted, True)
		self.assertEqual(a.isActive1(), True)
		a.end1()
		self.assertEqual(a.hasStarted, False)
		self.assertEqual(a.isActive1(), False)
	
	def test_basic_with(self):
		a = self.newInstance()
		self.assertEqual(a.hasStarted, False)
		self.assertEqual(a.isActive1(), False)
		with a:
			self.assertEqual(a.hasStarted, True)
			self.assertEqual(a.isActive1(), True)
		self.assertEqual(a.hasStarted, False)
		self.assertEqual(a.isActive1(), False)
	
	def test_noUseOnce(self):
		a = self.newInstance()
		self.assertEqual(a.hasStarted, False)
		self.assertEqual(a.isActive1(), False)
		a.start1()
		self.assertEqual(a.hasStarted, True)
		self.assertEqual(a.isActive1(), True)
		a.end1()
		self.assertEqual(a.hasStarted, False)
		self.assertEqual(a.isActive1(), False)
		a.start1()
		self.assertEqual(a.hasStarted, True)
		self.assertEqual(a.isActive1(), True)
		a.end1()
		self.assertEqual(a.hasStarted, False)
		self.assertEqual(a.isActive1(), False)
	
	def test_noAllowStartWhileRunning(self):
		a = self.newInstance(allowStartWhileRunning=False)
		with a:
			self.assertRaises(Exception, a.start1)
	
	def test_allowStartWhileRunning(self):
		a = self.newInstance(allowStartWhileRunning=True)
		self.assertEqual(a.hasStarted, False)
		self.assertEqual(a.isActive1(), False)
		a.start1()
		self.assertEqual(a.hasStarted, True)
		self.assertEqual(a.isActive1(), True)
		a.start1()
		self.assertEqual(a.hasStarted, True)
		self.assertEqual(a.isActive1(), True)
		a.end1()
		self.assertEqual(a.hasStarted, False)
		self.assertEqual(a.isActive1(), False)
	
	def test_useOnce(self):
		a = self.newInstance(useOnce=True)
		with a:
			pass
		self.assertRaises(Exception, a.start1)
	
	def test_useOnce_allowStartWhileRunning(self):
		a = self.newInstance(useOnce=True, allowStartWhileRunning=True)
		with a:
			a.start1()
		self.assertRaises(Exception, a.start1)
