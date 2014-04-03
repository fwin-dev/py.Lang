# <a name="concurrency"></a>Concurrency

The `Concurrency` package provides a unified API for locks and semaphores, in addition to some useful utilities.

## The API

Different threading APIs and similar will generally have `lock` and `release` methods, along with possibly some other methods and functionality.
A unified API was made in order to smooth over these differences and fill in functionality that was missing, then implementations and utilities
were made to take advantage of it. The standardization includes:

* Standardized method names
* Standardized parameters for `lock` and `release` methods
* Standardized parameters for lock/semaphore constructor

Locks are a semaphore, but only allow 1 thing to lock on a resource at a given time. Since both locks and semaphores use the same API, you can
interchange both as needed.

1. Blocking acquire with `with` statement

		sem = Semaphore(timeout=None)	# substitute a real "Semaphore" class here - "Semaphore" is the abstract class
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

See the source for more parameters available on `acquire(...)` and further explanation of `timeout`.

The following convenience functions are also available:

* `getMaxSlots()`
* `getSlotsTakenByAnyone()`
	* `Anyone` refers to anything that has acquired the semaphore
* `getSlotsTakenBySelf()`
	* `Self` has different meanings depending on the implementation (could be in the same process, in the same thread, in the same machine, etc.)
* `getSlotsAvailable()`
* `hasAvailableSlot()`

Locks have the following additional functions for convenience:

* `isTakenByAnyone()`
* `isTakenBySelf()`

## Thread implementation

**Note: This has not been fully tested**

`Concurrency.Threading` contains an API adapter which uses python's built-in threads, but with the unified API:

	from Lang.Concurrency.Threading import Semaphore, Lock

## FCNTL filesystem lock implementation

Provides a filesystem-wide lock (typically meaning machine-wide since a filesystem is usually only mounted once, on one machine) based on file locking provided by unix `FCNTL`. You must give the lock a unique name to lock on:

	from Lang.Concurrency.FileSystem import FileLock_ByFCNTL
	sem = FileLock_ByFCNTL(lockName="foo")
	...

Unfortunately:
* It does not provide a full semaphore implementation (it's only a lock) due to underlying implementation.
* Forks of the current process have access to the current process' file handles, but the forked process does NOT keep the locks associated with the files. So be careful when forking!

Fortunately:
* The lock is automatically released by kernel if the program quits without releasing it.
* It's a simple implementation compared to some others.

See source code for more details.

## @useLock

Using this function decorator will automatically cause a lock to be acquired before executing the function, and released after the function exits:

	from Concurrency.decorators import useLock
	
	lockInstance = ?	# instantiate your favorite type of lock here
	@useLock(lockInstance)
	def foo():
		<do something>

## @processify

Using this function decorator will automatically cause the function to run inside a new python process:

	from Concurrency.Multiprocessing.decorators import processify
	
	@processify
	def foo():
		<do something>

* Note that the code is not run in parallel to the current process, so this is not for gaining any speed.
* Note that every argument and the return value must be picklable.
