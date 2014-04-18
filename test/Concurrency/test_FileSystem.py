from Lang.Concurrency import FileSystem
from . import test_Abstract, test_Abstract_Scope
from Lang.Concurrency.Multiprocessing.decorators import processify

import os
import unittest

class Test_Concurrency_Lock_FileSystem_ByFCNTL(test_Abstract_Scope.Concurrency_LockSemaphore_ProcessDependentMixin,
												test_Abstract.Concurrency_Lock, unittest.TestCase):
	def tearDown(self):
		for lock in (self._lockSemInstance_paramsOnAcquire, self._lockSemInstance_paramsPreAcquire):
			if os.path.exists(lock.getLockFilePath()):
				os.remove(lock.getLockFilePath())
	
	def getInstance_paramsOnAcquire(self):
		return FileSystem.FileLock_ByFCNTL(self.__class__.__name__)
	def getInstance_paramsPreAcquire(self):
		return FileSystem.FileLock_ByFCNTL(self.__class__.__name__ + " #2", timeout=None, exceptionOnNotAcquire=True)
	
	def test_acquireDuringForkNotAllowed(self):
		@processify
		def _testSecondInstance(lockSem):
			self._checkStatusFunctions(lockSem, 0, 1)
			return str(lockSem)
		
		firstInstance = self._lockSemInstance_paramsPreAcquire
		secondInstance = self.getInstance_paramsPreAcquire()	# should return same instance due to multiton
		
		self._checkStatusFunctions(firstInstance, 0)
		print(firstInstance)
		print(secondInstance)
		
		with firstInstance:
			print("acquired")
			print(firstInstance)
			self._checkStatusFunctions(firstInstance, 1, 1)
			
			with self.assertRaises(FileSystem.ForkException):	# an exception is thrown when a forked process inherits the file descriptor but not the lock associated with it (OS issue)
				print(_testSecondInstance(secondInstance))
