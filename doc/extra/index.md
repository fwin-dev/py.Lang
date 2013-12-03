Package description	{#mainpage}
===================

# Summary of functionality

This package provides a lot of miscellaneous things that probably should have been included in python's built-in
library but weren't, including:

* Various function/method utilities/tools
  * An abstract class method
  * Timing execution of a function with a decorator
  * A way to get the argument names and values of a function without using **kwargs or *args
  * A way to describe the argument and return types of functions, kind of similar to a statically typed language
* Various class utilities/tools
  * Getting the variables of a class instance with __slots__
* Various module and package utilities/tools (Is a module built in? In what file is it? etc.)
* Implementation of various structures to hold data
  * LIFO/Stack
  * Frozen dictionary
  * Ordered set
* A peekable iterator
* An improved differ, based on `difflib.SequenceMatcher`
* An improved ArgParser for parsing command line arguments
* A poor man's debug tracer when a better tracer isn't available (for example, when running a python script over ssh)
* Easy event handling with subscription/listening, including event logging
* Terminal/user interaction improvements

# Detailed functionality

## Function/method tools

### An abstract class method

The built in `abc.abstractmethod` decorator won't work if used in conjunction with a `classmethod` decorator.
Use this abstract method decorator instead:

	from Lang.FuncTools.Abstraction import abstractmethod
	
	@classmethod
	@abstractmethod
	def myFunction(...):
		asdf

Make sure that `abstractmethod` comes after `classmethod`, else you will get:
`AttributeError: 'classmethod' object has no attribute '__name__'`

### Timing execution of a function

`timeIt` is a function decorator, so with the function you want to time, do:

	from Lang.FuncTools import timeIt	
	
	@timeIt
	def myFunction(...):
		asdf

### Getting a function's arguments

Python provides `**kwargs` and `*args` to get a dictionary or list of a function's arguments, but this makes it hard
for IDEs and documentation generators to determine all possible arguments to the function. As an alternative to
`**kwargs` or `*args`, you can use the `getArgs()` method:

	from Lang.FuncTools import getArgs
	def myFunc(arg1, arg2):
		allArgs = getArgs()

This method uses python's built in `inspect` module to go up the stack and inspect arguments.

In the case above, `allArgs` will be a list of values, similar to as if `*args` was used. To get a dictionary of
argument names and values instead, similar to `**kwargs`, use `getArgs(useKwargFormat=True)`.

Note that `cls` and `self` are automatically ignored for class methods and instance methods.

### Describing a function's argument and return types

Some convenience classes are defined here that provide a thin, rough API for describing types. See the source in
`Lang.Function` for details.

## Class tools

### Getting the variables of a class instance with __slots__

This works the same as the built-in python function `vars()`, except it also works on slotted classes:

	from Lang.ClassTools import vars
	myClassVars = vars(MyClass())

## Details about python packages

Python can provide a lot of information about a package and a lot of different ways of loading packages, but
the functions and code to accomplish this is scattered. This `PkgUtil` module provides everything in one location.

	from PyPkgUtil import PkgUtil

### Is it built in?

A built in module is one who's source is not defined in a file.

	PkgUtil.isBuiltin(moduleObj)

### Is it included in a stock python distibution?

	PkgUtil.isStock(moduleObj)

### Is an object a module or a package?

	PkgUtil.isModule(obj)
	PkgUtil.isPackage(obj)

### Getting all modules and packages imported by a module

	PkgUtil.getImported_all(moduleObj, isRecursive)

Returns a flat list with all modules and packages.

### Getting all packages imported by a module

	PkgUtil.getImported_packages(moduleObj, isRecursive)

Returns a flat list.

### Full module path -> Relative module path

Convert the full file path of a module to a relative path, which can be used for importing:

	relPath = PkgUtil.convert_fullPathToRelative(fullPath)

### Object -> Full path

Get the full file path of a module or package object:

	fullPath = PkgUtil.convert_objectToFullPath(obj)

### Full path -> Object

Get the module or package object from a full path, aka import a module or package at the specified path:

	obj = PkgUtil.convert_fullPathToObject(fullPath)

### Name string -> Object

Import an object by its name:

	obj = PkgUtil.convert_nameToObject("moduleName")

### Object -> Name string

Get the name of a module or package:

	name = PkgUtil.convert_objectToName(obj)

## Structures

### LIFO/Stack

Python lists can be used as stacks, but they don't have the normal API that a stack does.

	from Lang.Struct import LIFOstack
	stack = LIFOstack()
	stack.push("a")
	element = stack.peek()
	element = stack.pop()

### Frozen dictionary

In the case where a hashable dictionary is needed, `FrozenDict` can be used. `FrozenDict` is just like a normal `dict`
except it cannot be modified.

	from Lang.Struct import FrozenDict
	dict_ = FrozenDict({"asdf": 1, "jkl": 2})

### Ordered set

The built-in python `set` is just like a `list`, except for 2 things:

- Sets can't contain duplicate elements
- Sets are unordered
 
However, there are some cases where an ordered set (aka a list with no duplicate elements) is desirable. For this, use
the `OrderedSet` provided here, which provides a similar implementation compared to the built-in `set`, but also provides
methods typically found in a list, such as `insert`/`insertAt`. Refer to the source and unit test for a list of all methods.

	from Lang.Struct import OrderedSet
	set_ = OrderedSet(range(1,10))

## Peekable iterator

Want to use an iterator for RAM usage concerns, but need to know the next element sometimes without advancing the
iterator? Then this "peekable iterator" implementation is for you! Just wrap any iterable inside a `PeekableIterable`.
That inner iterable is most likely a pure iterator itself (such as a generator), but it could also be anything that
implements `__iter__`.

	from Lang.Iter import PeekableIterable
	def asdf():
		for i in range(0,10):
			yield i
	nums = PeekableIterable(asdf())
	print(nums.next())		# advances the iterator
	print(nums.peek())		# peeks without advancing
	print(nums.hasNext())	# checks if there's a next element

## Improved differ

This differ builds upon `difflib.SequenceMatcher` which can diff any python objects with `__eq__` implemented, contained
within a list, tuple, etc. However, the built in class only provides methods for getting matching sets of indices which
refer to matching elements, leaving you to infer which indices don't match. It also doens't give you direct access to
elements that do or don't match. This differ adds all of that functionality. It also fixes:

- A bug in the built in differ where subsequent calls to `get_matching_blocks()` returns results in a different format
- Calculating the similarity ratio: The built in differ calculates this ratio taking both diff sides into account, but what's usually wanted is how much one side is similar/different compared to the other side, i.e. `(1 - ratio) / 2 + ratio`

	from Lang.Diff import SequenceMatcher
	diff = SequenceMatcher(tuple("aebcdef"), tuple("abbcdgef"))
	print(list(diff.get_matching_blocks()))
	print(list(diff.get_mismatching_blocks()))
	print(list(diff.get_matching_elems()))
	print(list(diff.get_mismatching_elems()))

	Prints the following:
	[BlockMatch(a={index=0,size=1}, b={index=0,size=1}), BlockMatch(a={index=2,size=3}, b={index=2,size=3}), BlockMatch(a={index=5,size=2}, b={index=6,size=2})]
	[BlockMismatch(a={index=1,size=1}, b={index=1,size=1}), BlockMismatch(a=None, b={index=5,size=1})]
	[ElemMatch(a=('a',), b=('a',)), ElemMatch(a=('b', 'c', 'd'), b=('b', 'c', 'd')), ElemMatch(a=('e', 'f'), b=('e', 'f'))]
	[ElemMismatch(a=('e',), b=('b',)), ElemMismatch(a=None, b=('g',))]

More functions are available, including:

- `getmatching()` and `getmismatching()`
  - These return structures with `.block` and `.elems` attributes containing both block indices and the elems which the block refers to
- `get_matching_elems_useOnce()` and `get_mismatching_elems_useOnce()`
  - These are the same as `get_matching_elems()` and `get_mismatching_elems()` except that they are generators instead of functions returning a list

## An improved ArgParser

In addition to the plethora of features in python's built in `ArgParser`, a few more are added in here:

- Improved help formatting, similar to `man`
- 3 way boolean (`True`, `False`, `None`)
- Required named parameters - the built in ArgParser only supports required positional arguments and optional named parameters

The new `ArgParser` uses the same interface as the old one, so see the built in `ArgParser` documentation.

Example:

	from Lang.ArgParser import ArgParser
    parser = ArgParser(argument_default=None, add_help=True, description="Adds a user to a linux machine")
    parser.add_argument("username")
	parser.add_argument("-p", "--password", required=False, help="Prompt for password if this is not given")
	parser.add_argument("-H", "--create-home", type=Bool3Way, required=True,
		help="Controls home directory creation for user. None uses the default behavior which varies between machines.")
	args = parser.parse_args()

## Poor man's debugger

Several arguments are available here. See the source for more details.

	from Lang.DebugTracer import setTraceOn
	setTraceOn()

## Event handling

For general event handling with event subscription and listeners, there is a proxy API. The proxy receives an event
(via a method call) and then calls any subscribers (aka receivers) to the event. In this implementation, a subscriber
subscribes to all events, but only chooses to implement the methods for the events that it is interested in. The proxy
checks each receiver to see if it has implemented the method, and if so, calls the method. All receivers can be
forced to implement all methods by setting `errorOnMethodNotFound=True`.

	from Lang.Events.Proxy import EventProxy, EventReceiver
	proxy = EventProxy(errorOnMethodNotFound=False)
	
	class Foo(EventReceiver):
		def someEvent(self, parametersOfEvent, moreParams=None):
			print("I was called")
	
	foo = Foo()
	proxy.addReceiver(foo)
	proxy.someEvent("abc", moreParams=123)

## Handling uncaught exceptions

When an uncaught exception happens, a special `notifyException` method will be called on each EventReceiver
automatically, if the method is implemented, with the exception instance and a traceback instance as parameters.
What you do with these parameters is up to you, but here is an example:

	class Foo(EventReceiver):
		def notifyException(self, exceptionInstance, tracebackInstance):
			import traceback
			tracebackStr = "".join(traceback.format_tb(tracebackInstance))
			exceptionStr = str(exceptionInstance)
			print(tracebackStr)
			print()
			print(exceptionStr)

This idea can be combined with event logging, shown below.
Also note that `errorOnMethodNotFound` has no effect on `notifyException`, as it is a special case.

### Event logging

Python has decent built in logging, but it doesn't follow standard object-oriented concepts where methods represent
actions, so the API is not ideal for recording different events in a heavily event based system, as there would need
to be a special, separate call to the logging API for every event. The logging API in `Lang.Events.Logging` fixes this.
It uses the event handling API shown above, where the `Logging` class is an `EventProxy`, and the loggers are
`EventReceiver`s.

#### Example using StdoutLogger

This is a very simplistic example of logging to stdout:

	from Lang.Events.Logging import Logging, StdoutLogger
	log = Logging(StdoutLogger)
	log.notifyMyEvent("details", "in", "arguments", "here")

#### Example using a custom logger and/or multiple loggers

When using multiple loggers, the function you call on the `Logging` instance will be called on every logger.

	from Lang.Events.Logging import Logging, LoggerAbstract, StdoutLogger
	class MyFileLog(LoggerAbstract):
		def __init__(self, filePath):
			super(MyLogger, self).__init__()
			self._filePath = filePath
		def notifyFolderCheck(self, folder):
			with open(self._filePath, "a") as file_:
				file_.write("Checking folder: " + folder)
	
	log = Logging((StdoutLogger, MyFileLog))
	log.notifyFolderCheck("folder/path/here")

## Terminal improvements

### Asking the user a question

	from Lang import Terminal
	if Terminal.askYesNo("Do you like Star Trek?") == True:
		print("Awesome!")
	else:
		print("Your nerd credit has been lowered")

### Using formatted text on the terminal

	from Lang.Terminal import FormattedText

`FormattedText` returns a subclass of the built in python `str` type. It adds terminal formatting codes when
the `str` function is called on it:

	boldStr = str(FormattedText("I'm in bold", bold=True))

`boldStr` will contain some funny looking characters which enable formatting, but these characters do not influence
any other function of the string. For example:

	char = boldStr[2]

will store `m` into `char`. Similarly, `len` and other functions will act the same as if the string were a direct
instantiation of `str`.
 
Many more text attributes are available, including coloring - see the source for more information.

### Tables

Printing tabular data to the terminal is very common. This implementation of a table has a couple extras with it.
Here is an example:

	from Terminal import Table
	table = Table()
	table.setColHeaders(("First Name", "Last Name Initial", "Number"))	# optional
	table.setColMaxLens([None] * 3)			# enables automatic column sizing for the 3 columns
	table.addRow(["Jesse", "C", str(1234)])	# explicitly convert all elements to strings
	table.printLive()						# prints all rows (and headers) that haven't been printed before

If another row is added to the table, another call to `printLive()` will only print only that new row.

