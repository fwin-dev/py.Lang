# <a name="functools"></a>FuncTools

A collection of function/method utilities/tools.

## An abstract class method

The built-in `abc.abstractmethod` decorator won't work if used in conjunction with a `classmethod` decorator.
Use this abstract method decorator instead:

	from Lang.FuncTools.Abstraction import abstractmethod
	
	@classmethod
	@abstractmethod
	def myFunction(...):
		asdf

Make sure that `abstractmethod` comes after `classmethod`, else you will get:

	`AttributeError: 'classmethod' object has no attribute '__name__'`

## Timing execution of a function

`timeIt` is a function decorator, so with the function you want to time, do:

	from Lang.FuncTools import timeIt	
	
	@timeIt
	def myFunction(...):
		asdf

## Getting a function's arguments

Python provides `**kwargs` and `*args` to get a dictionary or list of a function's arguments, but this makes it hard
for IDEs and documentation generators to determine all possible arguments to the function. As an alternative to
`**kwargs` or `*args`, you can specify all arguments explicitly and then use the `getArgs()` method:

	from Lang.FuncTools import getArgs
	def myFunc(arg1, arg2):
		allKwargs = getArgs()

This method uses python's built-in `inspect` module to go up the stack and inspect arguments.

In the case above, `allKwargs` will be a dict of parameter names and associated values, similar to as if `**kwargs` was used.

To get a list of positional values instead, similar to `*args`, use `getArgs(useKwargFormat=False)`.

To get both kwargs and args, use:

	args, kwargs = getArgs(useKwargFormat=None)

* Note that `cls` and `self` are automatically ignored for class methods and instance methods.
* Note that if there is a question of whether an argument is an arg or a kwarg, then kwarg is preferred.
