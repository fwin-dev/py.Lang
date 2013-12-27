from Lang.FuncTools import getArgs

import unittest

class Test_GetArgs(unittest.TestCase):
	def _getClassInstance(self, *getArgs_args, **getArgs_kwargs):
		class A:
			def test(self, a, b, c, d, *args, **kwargs):
				return getArgs(*getArgs_args, **getArgs_kwargs)
		return A()
	
	def test_args_noVarArgs(self):
		args = self._getClassInstance(useKwargFormat=False, includeVariableArgs=False).test(1, 2, 3, 4, 5, 6, foo=7, bar=8)
		self.assertEqual(args, (1,2,3,4))
	def test_args_includeVarArgs(self):
		args = self._getClassInstance(useKwargFormat=False).test(1, 2, 3, 4, 5, 6, foo=7, bar=8)
		self.assertEqual(args, (1,2,3,4,5,6))
	
	def test_kwargs_noVarKwargs(self):
		kwargs = self._getClassInstance(includeVariableArgs=False).test(1, 2, c=3, d=4, foo=5, bar=6)
		self.assertEqual(kwargs, {"a":1, "b":2, "c":3, "d":4})
	def test_kwargs_includeVarKwargs(self):
		kwargs = self._getClassInstance().test(1, 2, c=3, d=4, foo=5, bar=6)
		self.assertEqual(kwargs, {"a":1, "b":2, "c":3, "d":4, "foo":5, "bar":6})
	
	def test_all_noVarArgs(self):
		args, kwargs = self._getClassInstance(useKwargFormat=None, includeVariableArgs=False).test(1, 2, 3, 4, 5, 6, foo=7, bar=8)
		self.assertEqual(args, (5,6))
		self.assertEqual(kwargs, {"a":1, "b":2, "c":3, "d":4})
	def test_all_noVarKwargs(self):
		args, kwargs = self._getClassInstance(useKwargFormat=None, includeVariableArgs=False).test(1, 2, c=3, d=4, foo=5, bar=6)
		self.assertEqual(args, tuple())
		self.assertEqual(kwargs, {"a":1, "b":2, "c":3, "d":4})
	def test_all_varArgs(self):
		args, kwargs = self._getClassInstance(useKwargFormat=None).test(1, 2, 3, 4, 5, 6, f=7, g=8, foo=9, bar=10)
		self.assertEqual(args, (5,6))
		self.assertEqual(kwargs, {"a":1, "b":2, "c":3, "d":4, "f":7, "g":8, "foo":9, "bar":10})
