import inspect

def getArgs(useKwargFormat, numFramesAgo=1, excludeList=[]):
	"""
	@param useKwargFormat	bool:	If `True`, returns a dict of parameters and values. If `False`, returns a list of parameter values only
	"""
	frame = inspect.getouterframes(inspect.currentframe())[numFramesAgo][0]
	args, varargs, varkw, locals_ = inspect.getargvalues(frame)
	notArgs = set(locals_) - set(args)
	for notArg in notArgs:	del locals_[notArg]
	excludeList.append("self")
	excludeList.append("cls")
	finalLocals = {}
	for k in locals_:
		if k not in excludeList and locals_[k] != None:
			finalLocals[k] = locals_[k]
	if useKwargFormat:
		return finalLocals
	else:
		return [finalLocals[arg] for arg in args if arg in finalLocals]

###

from functools import wraps
from time import time

def timeIt(f):
	"""
	Time a function
	
	Example:
	@timeIt
	def yourFunc(...):
		asdf
	"""
	@wraps(f)
	def wrapper(*args, **kwds):
		start = time()
		result = f(*args, **kwds)
		elapsed = time() - start
		print(f.__name__ + " took " + str(round(elapsed, 4)) + " seconds to finish")
		return result
	return wrapper
