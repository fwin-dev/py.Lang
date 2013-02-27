from Lang.OrderedSet import OrderedSet

import unittest

class Test_HELD(unittest.TestCase):
	def test_index(self):
		set_ = OrderedSet("abcde")
		self.assertEqual(set_.index("a"), 0, "Failed to find element at beginning of set")
		self.assertEqual(set_.index("e"), 4, "Failed to find element at end of set")
		self.assertEqual(set_.index("c"), 2, "Failed to find element in middle of set")
	
	def test_insertBefore(self):
		set_ = OrderedSet("bd")
		set_.insertBefore("c", "d", updateOnExist = True)
		self.assertEqual(set_, OrderedSet("bcd"), "Failed to insert an element before another")
		set_.insertBefore("a", "b", updateOnExist = True)
		self.assertEqual(set_, OrderedSet("abcd"), "Failed to insert an element before the first in the set")
	
	def test_insertBefore_updateOnExist(self):
		set_ = OrderedSet("bdace")
		set_.insertBefore("c", "d", updateOnExist = True)
		self.assertEqual(set_, OrderedSet("bcdae"), "Failed to insert an existing element before another")
		
		set_.insertBefore("a", "b", updateOnExist = True)
		self.assertEqual(set_, OrderedSet("abcde"), "Failed to insert an existing element before the first in the set")
		
		set_.insertBefore("d", "c", updateOnExist = False)
		self.assertEqual(set_, OrderedSet("abcde"), "Set changed on single insert when updateOnExist=False")
	
	def test_insertBeforeMulti(self):
		set_ = OrderedSet("dgi")
		set_.insertMultiBefore("h", "i", updateOnExist = True)
		self.assertEqual(set_, OrderedSet("dghi"), "Failed to insert a single element using insertMultiBefore")
		
		set_.insertMultiBefore(("e","f"), "g", updateOnExist = True)
		self.assertEqual(set_, OrderedSet("defghi"), "Failed to insert multiple elements in the set")
		
		set_.insertMultiBefore(("a","b","c"), "d", updateOnExist = True)
		self.assertEqual(set_, OrderedSet("abcdefghi"), "Failed to insert multiple elements before the first element in the set")
	
	def test_insertBeforeMulti_updateOnExist(self):
		set_ = OrderedSet("efdg")
		set_.insertMultiBefore(("e","f"), "g", updateOnExist = False)
		self.assertEqual(set_, OrderedSet("efdg"), "Set changed on multiple insert when updateOnExist=False")
		
		set_ = OrderedSet("edg")
		set_.insertMultiBefore(("e","f"), "g", updateOnExist = False)
		self.assertEqual(set_, OrderedSet("edfg"), "Incorrect set with multiple insert where some elements already exist")
	
	def test_append(self):
		set_ = OrderedSet("bc")
		set_.append("d", updateOnExist = True)
		self.assertEqual(set_, OrderedSet("bcd"), "Failed to replace and append an element")
		set_.append("b", updateOnExist = False)
		self.assertEqual(set_, OrderedSet("bcd"), "Set changed on append when updateOnExist=False")
	
	def test_getitem(self):
		set_ = OrderedSet("abc")
		self.assertEqual(set_[0], "a", "Lookup element by positive index failed")
		self.assertEqual(set_[1], "b", "Lookup element by positive index failed")
		self.assertRaises(KeyError, set_.__getitem__, 3)
		
		self.assertEqual(set_[-1], "c", "Lookup element by negative index failed")
		self.assertEqual(set_[-2], "b", "Lookup element by negative index failed")
		self.assertRaises(KeyError, set_.__getitem__, -4)
	
	def test_getitem_slice(self):
		set_ = OrderedSet("abcdef")
		self.assertEqual(set_[0:2], "ab", "Lookup elements by +:+ slice failed")
		self.assertEqual(set_[1:-1], OrderedSet("bcde"), "Lookup elements by +:- slice failed")
		self.assertEqual(set_[-3:-1], OrderedSet("de"), "Lookup elements by -:- slice failed")


if __name__ == "__main__":
	unittest.main()
