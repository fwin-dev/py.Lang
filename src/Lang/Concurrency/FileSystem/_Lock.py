from Lang.Concurrency import abstract
from Lang.ClassTools.Patterns import Multiton_OneEquivalentInstance_OnDupReturnExisting

import fcntl
import errno
import tempfile
from base64 import urlsafe_b64encode
from zlib import crc32
import os.path
import os

class FileLock_ByFCNTL(abstract.Lock, Multiton_OneEquivalentInstance_OnDupReturnExisting):
	"""
	Pros of this solution:
	- Lock is automatically released by kernel if program quits without releasing it
	- Simple implementation compared to some others
	
	Cons:
	- Forks of the current process have access to the current process' file handles, but the forked process does NOT keep the locks associated with the files. So be careful when forking!
	
	This is implemented by using `lockf` in python, which corresponds to `fcntl` in C:
	- http://docs.python.org/2/library/fcntl.html#fcntl.lockf
	- http://oilq.org/fr/node/13344
	"""
	def __init__(self, lockName, lockFolder=tempfile.gettempdir(), *args, **kwargs):
		super(FileLock_ByFCNTL, self).__init__(*args, **kwargs)
		self.lockName = lockName
		self.lockFolder = str(lockFolder)
		
		self._pid = os.getpid()
		self._in_checkForkSafety = False
		_fileName = str(crc32(self.lockName)) + "=" + urlsafe_b64encode(self.lockName) + ".lock"
		self._filePath = os.path.join(self.lockFolder, _fileName)
		self._file = None
	
	def __eq__(self, other):
		self._checkForkSafety()		# because __getattribute__ is not called when special methods are called in new style classes
		return isinstance(other, self.__class__) and self.lockName == other.lockName and self.lockFolder == other.lockFolder and self._pid == other._pid
	
	def __getattribute__(self, name):
		if name != "_in_checkForkSafety" and not self._in_checkForkSafety:
			self._in_checkForkSafety = True
			self._checkForkSafety()
			self._in_checkForkSafety = False
		return super(FileLock_ByFCNTL, self).__getattribute__(name)
	
	def _checkForkSafety(self):
		if self._pid != os.getpid():
			if self.getSlotsTakenBySelf() > 0:
				raise Exception("ERROR: This FCNTL lock was duplicated during a process fork, but the lock did not (and can not) carry over. The lock must be released before the fork, and acquired after the fork.")
			self._pid = os.getpid()
	
	def _acquire(self, shouldBlock):
		"""
		@param timeout:	Maximum time to wait, in seconds. Can be fractional. `0` will be non-blocking and return immediately. `None` means wait/block infinitely.
		http://docs.python.org/2/library/threading.html#threading.Lock.acquire
		
		After implementing this function, I also found another method using a second file descriptor with append (called `method_1`):
		http://www.gossamer-threads.com/lists/python/python/658463?do=post_view_threaded
		"""
		# FCNTL locks are not carried over when a process is forked, but there was no lock during the fork, so this is ok - just update the pid
		self._file = open(self._filePath, "w")
		if shouldBlock:
			fcntl.lockf(self._file.fileno(), fcntl.LOCK_EX)
		else:
			try:
				fcntl.lockf(self._file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError as err:
				if err.errno in (errno.EACCES, errno.EAGAIN):
					return False
				raise err
		return True
	
	def getLockFilePath(self):
		return self._filePath
	
	def getSlotsTakenByAnyone(self):
		if self.getSlotsTakenBySelf() == 1:		# bypasses filesystem, since we know it can only be held once at a time
			return 1
		# if not taken by self, then self._file doesn't exist
		if self._acquire(shouldBlock=False) == True:
			self._release()
			return 0
		return 1
	
	def _release(self):
		"""
		http://docs.python.org/2/library/threading.html#threading.Lock.release
		"""
		# fcntl.lockf(self._file, fcntl.LOCK_UN)		# this is not actually needed because the file will be unlocked when it's closed
		os.remove(self._filePath)
		self._file.close()
		self._file = None

FileLock = FileLock_ByFCNTL
