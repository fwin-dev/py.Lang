from __future__ import division
from abc import ABCMeta, abstractmethod
import time

from . import ResourceIsFullException, ResourceAlreadyReleasedException

class LockSemaphore(object):
	"""
	There are multiple ways to use subclasses of this class:
	
	1. Blocking acquire with `with` statement
	
		sem = Semaphore(timeout=None)
		with sem:
			# locked code here
	
	2. Nonblocking or partially blocking acquire with `with` statement and check for exception
	
		sem = Semaphore(timeout=0)		# exceptionOnNotAcquire is `True` by default
		try:
			with sem:
				# locked code here
		except ResourceIsFullException:
			# error handling here
	
	3. Blocking acquire using `acquire(...)` and `release(...)`
	
		sem = Semaphore(exceptionOnNotAcquire=False)
		if sem.acquire(timeout=None) == False:
			raise Exception("Could not acquire")
		# locked code here
		
		try:
			# locked code here
		except:
			# do something
		finally:
			sem.release()	# in case of some exception in the locked code, be sure to always release the lock
	
	4. Blocking acquire using `acquire(...)` and `release(...)` and check for exception
	
		sem = Semaphore()		# exceptionOnNotAcquire is `True` by default
		try:
			sem.acquire(timeout=None):
		except ResourceIsFullException:
			# error handling here
		
		try:
			# locked code here
		except:
			# do something
		finally:
			sem.release()	# in case of an exception other than `ResourceIsFullException`, be sure to always release the lock
	"""
	__metaclass__ = ABCMeta
	
	def __init__(self, maxSlots=1, *args, **kwargs):
		"""
		@param timeout: If given, the `with` statement can be used, and `timeout` does not have to be given in the `acquire` call
		@param *args, **kwargs:	If `with` statements are used, these are additional values passed into `acquire`
		"""
		super(LockSemaphore, self).__init__()
		self._maxSlots = maxSlots
		self._slotsAcquiredBySelf = 0
		
		if "timeout" in kwargs:
			self._acquireArgs = args
			self._acquireKwargs = kwargs
	def __str__(self):
		return self.__class__.__name__ + " instance " + str(id(self)) + ": " + str(self.getSlotsTakenBySelf()) + "/" + str(self.getMaxSlots()) + " taken by self, " + \
			str(self.getSlotsTakenByAnyone()) + "/" + str(self.getMaxSlots()) + " taken by everyone"
	
	def __getstate__(self):
		print("__getstate__")
		if self.getSlotsTakenBySelf() != 0:
			raise Exception("In order to be able to pickle this semaphore, it must be unacquired/released first")
		return super(LockSemaphore, self).__getstate__()
	
	@abstractmethod
	def __eq__(self, other):
		pass
	def __ne__(self, other):
		return not self.__eq__(other)
	
	@abstractmethod
	def getMaxSlots(self):
		pass
	@abstractmethod
	def getSlotsTakenByAnyone(self):
		pass
	def getSlotsTakenBySelf(self):
		return self._slotsAcquiredBySelf
	
	def getSlotsAvailable(self):
		slotsAvailable = self.getMaxSlots() - self.getSlotsTakenByAnyone()
		assert slotsAvailable >= 0
		return slotsAvailable
	def hasAvailableSlot(self):
		return self.getSlotsAvailable() > 0
	
	def acquire(self, timeout=None, exceptionOnNotAcquire=True, *args, **kwargs):
		"""
		*args and **kwargs are for optional/implementation specific parameters. If using them, there should always be a default value for all parameters.
		
		@param timeout:		Maximum time to wait, in seconds. Can be fractional. `0` will be non-blocking and return immediately. `None` means wait/block infinitely.
		@param exceptionOnNotAcquire:	If `timeout` is not `None` and the semaphore could not be acquired because it's full, look at this parameter on how to handle this situation. If this parameter is `True`, a `ResourceIsFullException` is raised; if `False`, the method does not raise an exception and instead returns `False`.
		
		@return:	`True` if semaphore is acquired, or `False` if all slots already taken
		
		@raise ResourceIsFullException:	If the semaphore could not be acquired because it's already in use and `exceptionOnNotAcquire` is `True`.
		
		If an underlying unusual exception occurs during acquirement of the semaphore, that exception will always be raised, regardless of the value of `exceptionOnNotAcquire`.
		"""
		if not self.hasAvailableSlot():
			raise ResourceIsFullException()
		
		if timeout in (None, 0):
			if timeout == None:	shouldBlock = True
			else:				shouldBlock = False
			
			wasAcquired = self._acquire(shouldBlock=shouldBlock, *args, **kwargs)
			if not wasAcquired and exceptionOnNotAcquire:
				raise ResourceIsFullException()
			if wasAcquired:
				self._slotsAcquiredBySelf += 1
			return wasAcquired
		else:
			sleepTime = min(0.1, timeout/10)
			elapsedTime = 0
			while True:
				currentTimeStart = time.clock()
				if self._acquire(shouldBlock=False, *args, **kwargs) == True:
					self._slotsAcquiredBySelf += 1
					return True
				time.sleep(sleepTime)
				elapsedTime += time.clock() - currentTimeStart
				if elapsedTime >= timeout:
					if exceptionOnNotAcquire:
						raise ResourceIsFullException()
					return False
	
	@abstractmethod
	def _acquire(self, shouldBlock, *args, **kwargs):
		"""@see `acquire`"""
		pass
	
	def release(self, *args, **kwargs):
		"""
		*args and **kwargs are for optional/implementation specific parameters. If using them, there should always be a default value for all parameters.
		
		@return By default, there is no return value. However, subclasses can opt to return something if needed.
		"""
		if self.getSlotsTakenBySelf() == 0:
			raise ResourceAlreadyReleasedException()
		ret = self._release(*args, **kwargs)
		self._slotsAcquiredBySelf -= 1
		return ret
	
	@abstractmethod
	def _release(self, *args, **kwargs):
		"""@see `release`"""
		pass
	
	def __enter__(self):
		if not hasattr(self, "_acquireKwargs"):
			raise Exception("In order to use a semaphore with the `with` statement, you must pass a `timeout` value to the constructor, along with any other parameters used by `acquire(...)`.")
		self.acquire(*(self._acquireArgs), **(self._acquireKwargs))
		return self
	def __exit__(self, *args, **kwargs):
		self.release()
		return False

class Semaphore(LockSemaphore):
	pass

class Lock(LockSemaphore):
	def __init__(self, *args, **kwargs):
		super(Lock, self).__init__(maxSlots=1, *args, **kwargs)
	def getMaxSlots(self):
		return 1
	
	def isAcquiredByAnyone(self):
		slotsTaken = self.getSlotsTakenByAnyone()
		assert 0 <= slotsTaken <= 1
		return (slotsTaken == 1)
	def isAcquiredBySelf(self):
		slotsTaken = self.getSlotsTakenBySelf()
		assert 0 <= slotsTaken <= 1
		return (slotsTaken == 1)
