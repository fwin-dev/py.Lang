import functools

def useLock(lockInstance, *acquireArgs, **acquireKwargs):
	"""
	Usage:
		@useLock(lockInstance)
		def myname(...):
			 ...
	"""
	def decor(func):
		@functools.wraps(func)
		def wrapper(*funcArgs, **funcKwargs):
			lockInstance.acquire(*acquireArgs, **acquireKwargs)
			try:
				return func(*funcArgs, **funcKwargs)
			finally:
				lockInstance.release()
		return wrapper
	return decor

useSemaphore = useLock
