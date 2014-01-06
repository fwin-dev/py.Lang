import threading
import abstract
from abc import ABCMeta, abstractmethod

class _ThreadingAdapter(object):
	__metaclass__ = ABCMeta
	def __init__(self, *args, **kwargs):
# 		print("_ThreadingAdapter.__init__")
		super(_ThreadingAdapter, self).__init__(*args, **kwargs)
		self._superclass = self._makeSuperclass()
	@abstractmethod
	def _makeSuperclass(self):
		pass
	def __getattr__(self, name):
		return getattr(self._superclass, name)
	
	# These must be manually stated here because `@abstractmethod` is not smart enough to use __getattr__
	def _acquire(self, shouldBlock, *args, **kwargs):
		"""http://docs.python.org/2/library/threading.html#threading.Lock.acquire"""
		return self.__getattr__("acquire")(blocking=shouldBlock, *args, **kwargs)
	def _release(self, *args, **kwargs):
		"""http://docs.python.org/2/library/threading.html#threading.Lock.release"""
		return self.__getattr__("release")(*args, **kwargs)

class Semaphore(_ThreadingAdapter, abstract.Semaphore):
	def _makeSuperclass(self):
		return threading.Semaphore(value=self._maxSlots)

class Lock(_ThreadingAdapter, abstract.Lock):
	def _makeSuperclass(self):
		"""The builtin `threading` module has a special implementation for a `Lock`, so use that"""
		return threading.Lock()
