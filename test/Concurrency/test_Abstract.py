from Lang.Concurrency import abstract, decorators, ResourceAlreadyReleasedException

import time
from abc import ABCMeta, abstractmethod

class Concurrency_LockSemaphore_Abstract(object):
	__metaclass__ = ABCMeta
	@abstractmethod
	def getInstance_paramsOnAcquire(self):
		pass
	@abstractmethod
	def getInstance_paramsPreAcquire(self):
		"""Should return an instance with `timeout=None`"""
		pass
	def setUp(self):
		self._lockSemInstance_paramsOnAcquire = self.getInstance_paramsOnAcquire()
		self._lockSemInstance_paramsPreAcquire = self.getInstance_paramsPreAcquire()
	
	def test_equals(self):
		self.assertEqual(self._lockSemInstance_paramsOnAcquire, self.getInstance_paramsOnAcquire())
		self.assertEqual(self._lockSemInstance_paramsPreAcquire, self.getInstance_paramsPreAcquire())
	
	def _checkStatusFunctions(self, lockSem, slotsTakenBySelf, slotsTakenByAnyone=None):
		if slotsTakenByAnyone == None:
			slotsTakenByAnyone = slotsTakenBySelf
		numAvailable = lockSem.getMaxSlots() - slotsTakenByAnyone
		
		self.assertEqual(lockSem.getSlotsTakenByAnyone(), slotsTakenByAnyone)
		self.assertEqual(lockSem.getSlotsTakenBySelf(), slotsTakenBySelf)
		self.assertEqual(lockSem.hasAvailableSlot(), numAvailable > 0)
		self.assertEqual(lockSem.isTakenByAnyone(), (slotsTakenByAnyone >= 1))
		self.assertEqual(lockSem.isTakenBySelf(), (slotsTakenBySelf >= 1))
	
	def testDecorator_basic(self):
		@self.decoratorFunc(self._lockSemInstance_paramsPreAcquire)
		def lockedCode():
			self._checkStatusFunctions(self._lockSemInstance_paramsPreAcquire, 1)
			time.sleep(0.1)
		self._checkStatusFunctions(self._lockSemInstance_paramsPreAcquire, 0)
		lockedCode()
		self._checkStatusFunctions(self._lockSemInstance_paramsPreAcquire, 0)
	
	def test_blocking_withStatement(self):
		self._checkStatusFunctions(self._lockSemInstance_paramsPreAcquire, 0)
		with self._lockSemInstance_paramsPreAcquire:
			self._checkStatusFunctions(self._lockSemInstance_paramsPreAcquire, 1)
			time.sleep(0.1)
		self._checkStatusFunctions(self._lockSemInstance_paramsPreAcquire, 0)
	
	def test_blocking_withStatement_repeatability(self):
		self.test_blocking_withStatement()
		self.test_blocking_withStatement()
	
	def test_blocking_acquireRelease(self):
		self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, 0)
		self._lockSemInstance_paramsOnAcquire.acquire(timeout=None)	# wait forever
		self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, 1)
		self._lockSemInstance_paramsOnAcquire.release()
		self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, 0)
	
	def test_blocking_acquireRelease_repeatability(self):
		self.test_blocking_acquireRelease()
		self.test_blocking_acquireRelease()
	
	def test_nonblocking_acquireRelease(self):
		self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, 0)
		try:
			self._lockSemInstance_paramsOnAcquire.acquire(timeout=0)
			self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, 1)
		finally:
			self._lockSemInstance_paramsOnAcquire.release()
			self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, 0)
	
	def test_nonblocking_acquireRelease_releaseTooMany(self):
		self.test_nonblocking_acquireRelease()
		self.assertRaises(ResourceAlreadyReleasedException, self._lockSemInstance_paramsOnAcquire.release)
		self._checkStatusFunctions(self._lockSemInstance_paramsOnAcquire, 0)

class Concurrency_Lock(Concurrency_LockSemaphore_Abstract):
	def setUp(self):
		super(Concurrency_Lock, self).setUp()
		assert isinstance(self._lockSemInstance_paramsOnAcquire, abstract.Lock)
	
	decoratorFunc = lambda self, *args, **kwargs: decorators.useLock(*args, **kwargs)
	
	def _checkStatusFunctions(self, lockSem, slotsTakenBySelf, slotsTakenByAnyone=None):
		if slotsTakenByAnyone == None:
			slotsTakenByAnyone = slotsTakenBySelf
		self.assertEqual(lockSem.getMaxSlots(), 1)
		super(Concurrency_Lock, self)._checkStatusFunctions(lockSem, slotsTakenBySelf, slotsTakenByAnyone)

class Concurrency_Semaphore(Concurrency_LockSemaphore_Abstract):
	def setUp(self):
		super(Concurrency_Lock, self).setUp()
		assert isinstance(self._lockSemInstance_paramsOnAcquire, abstract.Semaphore)
	
	decoratorFunc = lambda self, *args, **kwargs: decorators.useSemaphore(*args, **kwargs)
	
	def _checkStatusFunctions(self, lockSem, slotsTakenBySelf, slotsTakenByAnyone=None):
		if slotsTakenByAnyone == None:
			slotsTakenByAnyone = slotsTakenBySelf
		self.assertTrue(lockSem.getMaxSlots() >= 1)
		super(Concurrency_Lock, self)._checkStatusFunctions(lockSem, slotsTakenBySelf, slotsTakenByAnyone)
	
	def test_blocking_concurrency(self):
		assert self._lockSemInstance_paramsOnAcquire.getMaxSlots() > 1
		with self._lockSemInstance_paramsOnAcquire:
			with self._lockSemInstance_paramsOnAcquire:
				time.sleep(0.1)
