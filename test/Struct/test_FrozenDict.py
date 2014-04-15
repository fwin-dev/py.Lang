from Lang.Struct import FrozenDict

import unittest

class Test_FrozenDict(unittest.TestCase):
	def test_equal(self):
		dict_ = {"a":1, "b":2, "c":3}
		frozenDict = FrozenDict(dict_)
		self.assertEqual(dict_, frozenDict)
	
	def test_nestedDict(self):
		frozenDict = FrozenDict({"a": {"c":3, "d":4},
								 "b": {"e":5, "f":6}
								})
		self.assertTrue(isinstance(frozenDict["a"], FrozenDict))
		self.assertTrue(isinstance(frozenDict["b"], FrozenDict))
	
	def test_nestedList(self):
		frozenDict = FrozenDict({"a": ["c", "d"],
								 "b": ["e", "f"]
								})
		self.assertTrue(isinstance(frozenDict["a"], tuple))
		self.assertTrue(isinstance(frozenDict["b"], tuple))
	
	def test_hash(self):
		self.assertEqual(hash(FrozenDict({"a":1, "b":2, "c":3})), hash(FrozenDict({"a":1, "b":2, "c":3})))
	
	def test_toString(self):
		"""This is for code coverage only"""
		str(FrozenDict())
		str(FrozenDict({"a":1, "b":2, "c":3}))
		repr(FrozenDict({"a":1, "b":2, "c":3}))

if __name__ == "__main__":
	unittest.main()
