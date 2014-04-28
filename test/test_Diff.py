from __future__ import division
from Lang.Diff import SequenceMatcher
from types import GeneratorType
import unittest

class Test_SequenceMatcher(unittest.TestCase):
	def test_constructor_args(self):
		diffWithArgs = SequenceMatcher("abcdef", "abcdef")
		diffWithKwargs = SequenceMatcher("abcdef", "abcdef")
		self.assertEqual(diffWithArgs, diffWithKwargs)
	
	def test_ratio(self):
		self.assertEqual(SequenceMatcher(a="abcdef", b="abcdef").ratio(), 1)
		self.assertEqual(SequenceMatcher(a="abcdefg", b="cefhi").ratio(), 1 - 3/(7+5))
	
	def test_same_blocks(self):
		diff = SequenceMatcher(a="abcdef", b="abcdef")
		self.assertIsInstance(diff.get_matching_blocks(), GeneratorType)
		blocks = [i for i in diff.get_matching_blocks()]
		self.assertEqual(len(blocks), 1)
		self.assertEqual(blocks[0].a.index, 0)
		self.assertEqual(blocks[0].a.size,  6)
		self.assertEqual(blocks[0].b.index, 0)
		self.assertEqual(blocks[0].b.size,  6)
		
		self.assertIsInstance(diff.get_mismatching_blocks(), GeneratorType)
		blocks = [i for i in diff.get_mismatching_blocks()]
		self.assertEqual(len(blocks), 0)
	
	def test_same_elems(self):
		diff = SequenceMatcher(a="abcdef", b="abcdef")
		self.assertIsInstance(diff.get_matching_elems(), list)
		elems = diff.get_matching_elems()
		self.assertEqual(len(elems), 1)
		self.assertIsInstance(elems[0].a, tuple)
		self.assertIsInstance(elems[0].b, tuple)
		self.assertEqual(elems[0].a, tuple("abcdef"))
		self.assertEqual(elems[0].b, tuple("abcdef"))
		
		self.assertIsInstance(diff.get_matching_elems_useOnce(), GeneratorType)
		elems = [i for i in diff.get_matching_elems_useOnce()]
		self.assertEqual(len(elems), 1)
		
		# check inner types
		self.assertIsInstance(elems[0].a, GeneratorType)
		self.assertIsInstance(elems[0].b, GeneratorType)
		
		self.assertIsInstance(diff.get_mismatching_elems(), list)
		elems = diff.get_mismatching_elems()
		self.assertEqual(len(elems), 0)
		
		self.assertIsInstance(diff.get_mismatching_elems_useOnce(), GeneratorType)
		elems = [i for i in diff.get_mismatching_elems_useOnce()]
		self.assertEqual(len(elems), 0)
	
	def test_missing_blocks(self):
		diff = SequenceMatcher(a="abcdefg", b="cefhi")
		self.assertEqual(diff.ratio(), 1 - 3/(7+5))
		
		self.assertIsInstance(diff.get_matching_blocks(), GeneratorType)
		blocks = [i for i in diff.get_matching_blocks()]
		self.assertEqual(len(blocks), 2)
		self.assertEqual(blocks[0].a.index, 2)
		self.assertEqual(blocks[0].a.size,  1)
		self.assertEqual(blocks[0].b.index, 0)
		self.assertEqual(blocks[0].b.size,  1)
		self.assertEqual(blocks[1].a.index, 4)
		self.assertEqual(blocks[1].a.size,  2)
		self.assertEqual(blocks[1].b.index, 1)
		self.assertEqual(blocks[1].b.size,  2)
		
		self.assertIsInstance(diff.get_mismatching_blocks(), GeneratorType)
		blocks = [i for i in diff.get_mismatching_blocks()]
		self.assertEqual(len(blocks), 3)
		self.assertEqual(blocks[0].a.index, 0)
		self.assertEqual(blocks[0].a.size,  2)
		self.assertEqual(blocks[0].b, None)
		self.assertEqual(blocks[1].a.index, 3)
		self.assertEqual(blocks[1].a.size,  1)
		self.assertEqual(blocks[1].b, None)
		self.assertEqual(blocks[2].a.index, 6)
		self.assertEqual(blocks[2].a.size,  1)
		self.assertEqual(blocks[2].b.index, 3)
		self.assertEqual(blocks[2].b.size,  2)
	
	def test_missing_elems(self):
		diff = SequenceMatcher(a="abcdefg", b="cefhi")
		self.assertIsInstance(diff.get_matching_elems(), list)
		elems = diff.get_matching_elems()
		self.assertEqual(len(elems), 2)
		
		self.assertIsInstance(elems[0].a, tuple)
		self.assertIsInstance(elems[0].b, tuple)
		self.assertEqual(elems[0].a, tuple("c"))
		self.assertEqual(elems[0].b, tuple("c"))
		self.assertEqual(elems[1].a, tuple("ef"))
		self.assertEqual(elems[1].b, tuple("ef"))
		
		self.assertIsInstance(diff.get_matching_elems_useOnce(), GeneratorType)
		elems = [i for i in diff.get_matching_elems_useOnce()]
		self.assertEqual(len(elems), 2)
		
		# check inner types
		self.assertIsInstance(elems[0].a, GeneratorType)
		self.assertIsInstance(elems[0].b, GeneratorType)
		
		
		self.assertIsInstance(diff.get_mismatching_elems(), list)
		elems = diff.get_mismatching_elems()
		print(elems)
		self.assertEqual(len(elems), 3)
		self.assertEqual(elems[0].a, tuple("ab"))
		self.assertEqual(elems[0].b, None)
		self.assertEqual(elems[1].a, tuple("d"))
		self.assertEqual(elems[1].b, None)
		self.assertEqual(elems[2].a, tuple("g"))
		self.assertEqual(elems[2].b, tuple("hi"))
		
		self.assertIsInstance(diff.get_mismatching_elems_useOnce(), GeneratorType)
		elems = [i for i in diff.get_mismatching_elems_useOnce()]
		self.assertEqual(len(elems), 3)
