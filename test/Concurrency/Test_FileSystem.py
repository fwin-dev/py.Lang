from Lang import Concurrency
from . import Test_Abstract

import os
import unittest

class Test_Concurrency_Lock_FileSystem_ByFCNTL(Test_Abstract.Concurrency_LockSemaphore_ProcessDependentMixin,
												Test_Abstract.Concurrency_Lock, unittest.TestCase):
	def tearDown(self):
		for lock in (self._lockSemInstance_paramsOnAcquire, self._lockSemInstance_paramsPreAcquire):
			if os.path.exists(lock.getLockFilePath()):
				os.remove(lock.getLockFilePath())
	def getInstance_paramsOnAcquire(self):
		return Concurrency.FileSystem.FileLock_ByFCNTL(self.__class__.__name__)
	def getInstance_paramsPreAcquire(self):
		return Concurrency.FileSystem.FileLock_ByFCNTL(self.__class__.__name__ + " #2", timeout=None, exceptionOnNotAcquire=True)
