from Lang.Struct import LIFOstack

import unittest

class Test_LIFOstack(unittest.TestCase):
	def _constructStack(self):
		stack = LIFOstack()
		stack.push("a")
		stack.push("b")
		stack.push("c")
		stack.push("d")
		return stack
	
	def test_getItem(self):
		stack = self._constructStack()
		self.assertEqual(stack[2], "c")
	def test_setItem(self):
		stack = self._constructStack()
		stack[2] = "y"
		self.assertEqual(stack[2], "y")
	def test_push(self):
		self._constructStack()
	
	def test_peek(self):
		stack = self._constructStack()
		self.assertEqual(stack.peek(), "d")
		self.assertEqual(stack.peek(2), "c")
		self.assertEqual(stack.peek(-1), "b")
	def test_pop(self):
		stack = self._constructStack()
		self.assertEqual(stack.pop(), "d")
		self.assertEqual(stack.pop(), "c")
		self.assertEqual(stack.pop(), "b")
		self.assertEqual(stack.pop(), "a")
		self.assertRaises(IndexError, stack.pop)
	
	def test_len(self):
		self.assertEqual(len(self._constructStack()), 4)
	
	def test_equal(self):
		self.assertEqual(self._constructStack(), self._constructStack())
		stack2 = self._constructStack()
		stack2.push("e")
		self.assertNotEqual(self._constructStack(), stack2)
	
	def test_toString(self):
		"""This is for code coverage only"""
		str(LIFOstack())
		
		stack = LIFOstack()
		stack.push("a")
		stack.push("b")
		stack.push("c")
		str(stack)
		repr(stack)

if __name__ == "__main__":
	unittest.main()
