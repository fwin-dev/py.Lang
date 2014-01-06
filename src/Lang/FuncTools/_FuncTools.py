from Lang.Struct import OrderedDict
import inspect

def getArgs(useKwargFormat=True, includeVariableArgs=True, numFramesAgo=1, excludeList=[]):
	"""
	Magically returns function arguments in the function calling `getArgs`.
	
	If `useKwargFormat` is `True`, returns all keyword arguments in the calling function, as a dict of parameters and their values.
	Note that any positional arguments which can be bound to a keyword in the function definition will be returned by `getArgs` also.
	However, if an argument value must be positional and cannot be bound to a keyword, it will not be returned.
	
	If `useKwargFormat` is `False`, returns all arguments in the calling function as positional arguments, as a list of parameter values.
	This will exclude any values passed via `**kwargs`, as they have no position.
	
	If `useKwargFormat is `None`, returns both args and kwargs as a tuple `(args, kwargs)` which can be easily unpacked.
	If a parameter can be represented as both a positional and keyword argument, it will only be present in `kwargs`, as keyword arguments are favored/preferred.
	
	@param useKwargFormat		3 way bool:	Described in method docs
	@param includeVariableArgs	bool:		If `True`, either all *args or **kwargs are included in the returned list/dict, depending on the value of `useKwargFormat`.
	"""
	frame = inspect.getouterframes(inspect.currentframe())[numFramesAgo][0]
	argNames, varArgs_name, varKwargs_name, locals_ = inspect.getargvalues(frame)
	varArgs = locals_[varArgs_name] if varArgs_name != None else tuple()
	varKwargs = locals_[varKwargs_name] if varKwargs_name != None else {}
	notArgs = set(locals_.iterkeys()) - set(argNames)
	
	for notArg in notArgs:	del locals_[notArg]
	excludeList.append("self")
	excludeList.append("cls")
	mixedKwargsArgs = OrderedDict((argName, locals_[argName]) for argName in argNames if argName not in excludeList)
	
	if useKwargFormat == True:
		kwargs = dict(mixedKwargsArgs)
		if includeVariableArgs:
			kwargs.update(varKwargs)
		return kwargs
	elif useKwargFormat == False:
		args = tuple(mixedKwargsArgs.values())
		if includeVariableArgs:
			args += varArgs
		return args
	elif useKwargFormat == None:
		kwargs = dict(mixedKwargsArgs)
		if includeVariableArgs:
			kwargs.update(varKwargs)
		return varArgs, kwargs
	else:
		raise Exception("Invalid useKwargFormat")

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

