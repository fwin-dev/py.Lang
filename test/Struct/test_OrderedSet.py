from Lang.Struct import OrderedSet

import unittest

class Test_OrderedSet(unittest.TestCase):
	def test_index(self):
		set_ = OrderedSet("abcde")
		self.assertEqual(set_.index("a"), 0, "Failed to find element at beginning of set")
		self.assertEqual(set_.index("e"), 4, "Failed to find element at end of set")
		self.assertEqual(set_.index("c"), 2, "Failed to find element in middle of set")
	
	def test_toString(self):
		"""This is for code coverage only"""
		str(OrderedSet())
		str(OrderedSet("abcde"))
		repr(OrderedSet("abcde"))
	
	def test_contains(self):
		set_ = OrderedSet("bcd")
		self.assertTrue("b" in set_)
		self.assertTrue("a" not in set_)
	
	def test_pop(self):
		set_ = OrderedSet("bcd")
		self.assertEqual(set_.pop(), "d")
		self.assertEqual(set_.pop(), "c")
		self.assertEqual(set_.pop(), "b")
		self.assertRaises(KeyError, set_.pop)
	
	def test_insertAt(self):
		set_ = OrderedSet("bcd")
		set_.insertAt(0, "a")
		self.assertEqual(set_, OrderedSet("abcd"), "insertAt failed when inserting at the beginning of the set")
		
		set_ = OrderedSet("bcd")
		set_.insertAt(3, "e")
		self.assertEqual(set_, OrderedSet("bcde"), "insertAt failed when inserting at the end of the set")
		
		set_ = OrderedSet("abd")
		set_.insertAt(2, "c")
		self.assertEqual(set_, OrderedSet("abcd"), "insertAt failed when inserting in the middle of the set")
	
	def test_insertBefore(self):
		set_ = OrderedSet("bd")
		set_.insertBefore("c", "d", updateOnExist=True)
		self.assertEqual(set_, OrderedSet("bcd"), "Failed to insert an element before another")
		set_.insertBefore("a", "b", updateOnExist=True)
		self.assertEqual(set_, OrderedSet("abcd"), "Failed to insert an element before the first in the set")
	
	def test_insertBefore_updateOnExist(self):
		set_ = OrderedSet("bdace")
		set_.insertBefore("c", "d", updateOnExist=True)
		self.assertEqual(set_, OrderedSet("bcdae"), "Failed to insert an existing element before another")
		
		set_.insertBefore("a", "b", updateOnExist=True)
		self.assertEqual(set_, OrderedSet("abcde"), "Failed to insert an existing element before the first in the set")
		
		set_.insertBefore("d", "c", updateOnExist=False)
		self.assertEqual(set_, OrderedSet("abcde"), "Set changed on single insert when updateOnExist=False")
	
	def test_insertBeforeMulti(self):
		set_ = OrderedSet("dgi")
		set_.insertMultiBefore("h", "i", updateOnExist=True)
		self.assertEqual(set_, OrderedSet("dghi"), "Failed to insert a single element using insertMultiBefore")
		
		set_.insertMultiBefore(("e","f"), "g", updateOnExist=True)
		self.assertEqual(set_, OrderedSet("defghi"), "Failed to insert multiple elements in the set")
		
		set_.insertMultiBefore(("a","b","c"), "d", updateOnExist=True)
		self.assertEqual(set_, OrderedSet("abcdefghi"), "Failed to insert multiple elements before the first element in the set")
	
	def test_insertBeforeMulti_updateOnExist(self):
		set_ = OrderedSet("efdg")
		set_.insertMultiBefore(("e","f"), "g", updateOnExist=False)
		self.assertEqual(set_, OrderedSet("efdg"), "Set changed on multiple insert when updateOnExist=False")
		
		set_ = OrderedSet("edg")
		set_.insertMultiBefore(("e","f"), "g", updateOnExist=False)
		self.assertEqual(set_, OrderedSet("edfg"), "Incorrect set with multiple insert where some elements already exist")
	
	def test_append(self):
		set_ = OrderedSet("bc")
		set_.append("d", updateOnExist=True)
		self.assertEqual(set_, OrderedSet("bcd"), "Failed to replace and append an element")
		set_.append("b", updateOnExist=False)
		self.assertEqual(set_, OrderedSet("bcd"), "Set changed on append when updateOnExist=False")
	
	
	def test_getitem_index(self):
		set_ = OrderedSet("abc")
		self.assertEqual(set_[0], "a", "Lookup element by positive index failed")
		self.assertEqual(set_[1], "b", "Lookup element by positive index failed")
		self.assertRaises(KeyError, set_.__getitem__, 3)
		
		self.assertEqual(set_[-1], "c", "Lookup element by negative index failed")
		self.assertEqual(set_[-2], "b", "Lookup element by negative index failed")
		self.assertRaises(KeyError, set_.__getitem__, -4)
	
	def test_getitem_slice(self):
		set_ = OrderedSet("abcdef")
		self.assertEqual(set_[0:2], OrderedSet("ab"), "Lookup elements by +:+ slice failed")
		self.assertEqual(set_[0:0], OrderedSet(), "Lookup elements by 0:0 slice failed")
		self.assertEqual(set_[1:-1], OrderedSet("bcde"), "Lookup elements by +:- slice failed")
		self.assertEqual(set_[-3:-1], OrderedSet("de"), "Lookup elements by -:- slice failed")
	
	def test_delitem(self):
		set_ = OrderedSet("abcd")
		del set_[1]
		self.assertEqual(set_, OrderedSet("acd"), "Failed to delete item in middle of set")
		del set_[2]
		self.assertEqual(set_, OrderedSet("ac"), "Failed to delete item at end of set")
		del set_[0]
		self.assertEqual(set_, OrderedSet("c"), "Failed to delete item at beginning of set")
	
	def test_replace_byitem(self):
		set_ = OrderedSet("xyz")
		set_.replace("x", "a")
		self.assertEqual(set_, OrderedSet("ayz"), "Failed to change item at beginning of set")
		set_.replace("y", "b")
		self.assertEqual(set_, OrderedSet("abz"), "Failed to change item in middle of set")
		set_.replace("z", "c")
		self.assertEqual(set_, OrderedSet("abc"), "Failed to change item at end of set")
	
	def test_setitem_index(self):
		set_ = OrderedSet("abc")
		set_[0] = "x"
		self.assertEqual(set_, OrderedSet("xbc"), "Failed to change item at beginning of set")
		set_[2] = "z"
		self.assertEqual(set_, OrderedSet("xbz"), "Failed to change item at end of set")
		set_[1] = "y"
		self.assertEqual(set_, OrderedSet("xyz"), "Failed to change item in middle of set")
	
# 	def test_setitem_slice_insert(self):
# 		set_ = OrderedSet("abc")
# 		set_[3:3] = "o"
# 		self.assertEqual(set_, OrderedSet("abco"), "Failed to insert item at end of set")
# 		set_[1:1] = "o"
# 		self.assertEqual(set_, OrderedSet("aobco"), "Failed to insert item in middle of set")
# 		set_[0:0] = "o"
# 		self.assertEqual(set_, OrderedSet("oaobco"), "Failed to insert item at beginning of set")
	
# 	def test_setitems_slice(self):
# 		set_ = OrderedSet("abcd")
# 		set_[0:2] = ("w", "k")
# 		self.assertEqual(set_, OrderedSet("wkcd"), "Failed to change items, at beginning of set, by slice")
# 		set_[2:4] = ("l", "z")
# 		self.assertEqual(set_, OrderedSet("wklz"), "Failed to change items, at end of set, by slice")
# 		set_[1:3] = ("x", "y")
# 		self.assertEqual(set_, OrderedSet("wxyz"), "Failed to change items, in middle of set, by slice")

if __name__ == "__main__":
	unittest.main()
