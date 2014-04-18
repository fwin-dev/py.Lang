from Lang.Concurrency import ResourceIsFullException
from test_Abstract import Concurrency_LockSemaphore_Abstract

import time

class Concurrency_LockSemaphore_ProcessDependentMixin(Concurrency_LockSemaphore_Abstract):
	"""
	For locks or semaphores that acquire on a per-process basis.
	(ex. calling acquire twice on a lock by same process works the second time because the lock is already acquired by the process)
	"""
	pass

class Concurrency_LockSemaphore_NonProcessDependentMixin(Concurrency_LockSemaphore_Abstract):
	def test_nonblocking_acquireRelease_acquireTooMany(self):
		self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, 0)
		try:
			for i in range(1, self._lockSemInstance_paramsOnAcquire.getMaxSlots() + 1):
				self._lockSemInstance_paramsOnAcquire.acquire(timeout=None)
				self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, i)
			time.sleep(0.1)
			self.assertRaises(ResourceIsFullException, self._lockSemInstance_paramsOnAcquire.acquire, timeout=None)
			self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, self._lockSemInstance_paramsOnAcquire.getMaxSlots())
		finally:
			for i in range(self._lockSemInstance_paramsOnAcquire.getSlotsTakenByAnyone()-1, 0-1, -1):
				self._lockSemInstance_paramsOnAcquire.release()
				self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, i)
	
	def test_partialBlocking_acquireRelease(self):
		elapsedTime = self._test_concurrency_wait(timeout=0.1)
		self.assertGreaterEqual(elapsedTime, 0.1)
		self.assertLess(0.11)	# allow for some overhead here
	
	def test_blocking_concurrency_wait(self):
		self._test_concurrency_wait(timeout=None)
	
	def _test_concurrency_wait(self, timeout):
		self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, 0)
		try:
			for i in range(1, self._lockSemInstance_paramsOnAcquire.getMaxSlots() + 1):
				self._lockSemInstance_paramsOnAcquire.acquire(timeout=None)
				self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, i)
			time.sleep(0.1)
			startTime = time.clock()
			self.assertRaises(ResourceIsFullException, self._lockSemInstance_paramsOnAcquire.acquire, timeout=timeout)
			elapsedTime = time.clock() - startTime
			self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, self._lockSemInstance_paramsOnAcquire.getMaxSlots())
		finally:
			for i in range(self._lockSemInstance_paramsOnAcquire.getSlotsTakenByAnyone()-1, 0-1, -1):
				self._lockSemInstance_paramsOnAcquire.release()
				self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, i)
		return elapsedTime
