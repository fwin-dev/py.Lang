from Lang.Concurrency import Multiprocessing
import os

@Multiprocessing.decorators.processify
def _testSecondInstance(lockSem):
	print(os.getpid())
	return "foo"

class Foo(object):
	def __getstate__(self):
		print("getstate")
		return self.__dict__

print(os.getpid())
_testSecondInstance(Foo())
