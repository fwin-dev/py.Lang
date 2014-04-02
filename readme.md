Package description	{#mainpage}
===================

# Summary of functionality

This package provides a lot of miscellaneous things that probably should have been included in python's built-in
library but weren't, including:

* [FuncTools](#functools): Various function/method utilities/tools
	* `FuncTools.Abstraction.abstractmethod`: An abstract method that can be used with `@classmethod`
	* `FuncTools.timeIt`: Timing execution of a function with a decorator
	* `FuncTools.getArgs`: A way to get the argument names and values of a function without using `**kwargs` or `*args`
* [ClassTools](#classtools): Various utilities/tools for working with classes. Also includes class patterns.
	* `ClassTools.vars`: Getting the variables of a class instance with `__slots__`
	* `ClassTools.Patterns`: A package with implementations of [class patterns](http://en.wikipedia.org/wiki/Software_design_pattern)
		* `ClassTools.Patterns.RegisteredInstances`: Easily keep track of all instances of a class
		* `ClassTools.Patterns.Singleton`: Class bases (using metaclass) that implement the singleton pattern
		* `ClassTools.Patterns.Multiton`: Class bases (using metaclass) that implement the multiton pattern
		* `ClassTools.Patterns.StartEndWith`: Automatic support of the `with` statement by implementing only a start and end method
* [PyPkgUtil](#pypkgutil): Various module and package utilities/tools (Is a module built in? In what file is it? etc.)
* [Struct](#struct): Implementation of various structures to hold data
	* `Struct.LIFOstack`: LIFO/Stack
	* `Struct.FrozenDict`: Frozen dictionary
	* `Struct.OrderedSet`: Ordered set
* [Iter](#iter)
	* `Iter.PeekableIterable`: A peekable iterator
* [Diff](#diff)
	* `Diff.SequenceMatcher`: An improved differ, based on python's builtin `difflib.SequenceMatcher`
* [Concurrency](#concurrency): Unified API for locks, semaphores, etc., along with some useful tools/utilities
	* `Concurrency.Multiprocessing`: For dealing with multiple python processes
		* `Concurrency.Multiprocessing.decorators.processify`: Run a function in a separate process
	* `Concurrency.decorators.useLock`: Surround an entire function's execution in a lock
	* `Concurrency.Threading`: A lock and semaphore using standard python threads
	* `Concurrency.FileSystem.FileLock_ByFCNTL`: A lock using unix FCNTL file locking
* [Terminal](#terminal): Utilities for improving terminal interaction with the user
	* `Terminal.askYesNo`: A simple way of asking user to respond with yes or no
	* `Terminal.FormattedText`: Color text in the terminal. Also can do bold, underline, etc. depending on the terminal.
	* `Terminal.Table`: Nicely prints column+row data in the terminal.
	* `Terminal.ArgParser`: An improved ArgParser for parsing command line arguments
* [Events](#events): Easy event handling with subscriptions+callbacks, including an API for event logging
	* `Events.Proxy`: Provides a super easy API for event subscription and callbacks
	* `Events.Logging`: Skeleton classes for logging events to different destinations
* [DebugTracer](#debugtracer): A poor man's debug tracer when a better tracer isn't available (for example, when running a python script over ssh without remote debugging)

# Detailed functionality

## <a name="functools"></a>FuncTools

A collection of function/method utilities/tools.

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
`**kwargs` or `*args`, you can specify all arguments explicitly and then use the `getArgs()` method:

	from Lang.FuncTools import getArgs
	def myFunc(arg1, arg2):
		allKwargs = getArgs()

This method uses python's built in `inspect` module to go up the stack and inspect arguments.

In the case above, `allKwargs` will be a dict of parameter names and associated values, similar to as if `**kwargs` was used.

To get a list of positional values instead, similar to `*args`, use `getArgs(useKwargFormat=False)`.

To get both kwargs and args, use:

	args, kwargs = getArgs(useKwargFormat=None)

* Note that `cls` and `self` are automatically ignored for class methods and instance methods.
* Note that if there is a question of whether an argument is an arg or a kwarg, then kwarg is preferred.

## ClassTools

Various utilities/tools for working with classes. Also includes class patterns.

### Getting the variables of a class instance with __slots__

This works the same as the built-in python function `vars()`, except it also works on slotted classes:

	from Lang.ClassTools import vars
	myClassVars = vars(MyClass())

### Patterns

#### Keeping track of class instances

A common pattern in programming is the need to access all instantiations of a class for some reason. In static languages, this is
often done in a factory, but in python, we can use metaclasses to implement this, and it gives a nicer interface for the programmer.
For example:

	from Lang.ClassTools.Patterns import RegisteredInstances
	
	class Foo(RegisteredInstances):
		def __init__(self, value):
			super(Foo, self).__init__()
			self.value = value
	
	a = Foo("asdf")
	b = Foo("kjlh")
	
Now we can use the following to get an OrderedSet of all instances created:

	fooInstances = Foo.getAllInstances()

The `RegisteredInstances` superclass also aims to support subclasses of your `Foo` in a nice way. For example, if we additionally define:

	class Bar(Foo):
		pass

And then instantiate:

	c = Bar("iuhl")

We'll get the following results:
* A call to `Foo.getAllInstances()` will return an OrderedSet of all 3 instances (2 of `Foo`, 1 of `Bar`) instantiated up to this point.
* A call to `Foo.getAllClasses()` will return an iterable of 2 classes, `Foo` and `Bar`.
* A call to `Bar.getAllInstances()` will return an OrderedSet of 1 instance of `Bar`.
* A call to `Bar.getAllClasses()` will return an iterable of 1 class, `Bar`.

#### Singleton pattern

A well known pattern is [the singleton pattern](http://en.wikipedia.org/wiki/Singleton_pattern). There are two implementations available
in this package, depending on wanted behavior when your class's constructor is (incorrectly) called multiple times (aka `duplicate` instances);
one implementation will raise an exception for the second instantiation attempt, and the other will simply ignore and discard the second
attempt, and give the originally instantiated object back. Let's see these in action:

	from Lang.ClassTools.Patterns import Singleton_OnDupRaiseException
	
	class Foo(Singleton_OnDupRaiseException):
		def __init__(self, value):
			super(Foo, self).__init__()
			self.value = value
	a = Foo(1)
	b = Foo(2)	# an exception is raised

And the other singleton implementation:

	from Lang.ClassTools.Patterns import Singleton_OnDupReturnExisting
	
	class Foo(Singleton_OnDupReturnExisting):
		def __init__(self, value):
			super(Foo, self).__init__()
			self.value = value
	a = Foo(1)
	b = Foo(2)	# b actually holds the Foo(1) instance, and Foo(2) is not created

Note: Make sure the singleton superclass is the **first** in your MRO heirarchy.

The following methods would be available on `Foo`, similar to the "instance tracking" pattern, above. (See there for more details.)
Differences are noted here:
* `Foo.getAllClasses()`: Same behavior as above.
* `Foo.getAllInstances()`: Will return a dictionary with the key being the class, and the value being the singleton instance.

#### Multiton pattern

There are two implementations of [the multiton pattern](http://en.wikipedia.org/wiki/Multiton_pattern) aka "registry of singletons",
similar to the singleton pattern above. Although wikipedia says a multiton is simply a singleton that keeps track of instances via key+value
storage, this is very vague. In the py.Lang multiton implementation, each instance of the class must not be equal to another instance of the class
(hence the name `Multiton_OneEquivalentInstance`), else either an exception is raised, or the existing instance, which is equal, is returned
(hence the names `OnDupRaiseException`/`OnDupReturnExisting`, same as the singleton pattern). The uniqueness of the instance can be defined by
the `__eq__` method. However, unlike the singleton pattern, since the instance must be created in order to compare using `__eq__`, be careful
because the object's `__init__` method will always be called, regardless of whether the new instance is equal to an already-created instance.
This could introduce an unintended side effect if not known in advance. If the new instance is not in fact valid, then it will be deleted
(actually garbage collected because it will fall out of scope) after `__init__` and `__eq__` have been called.

The classes which can be inherited from are `Multiton_OneEquivalentInstance_OnDupRaiseException` and `Multiton_OneEquivalentInstance_OnDupReturnExisting`.  
Here is an example 2 instances allowed because the comparison is done by memory address, not using `__eq__`:

	class Foo(Multiton_OneEquivalentInstance_OnDupRaiseException):
		def __init__(self, value):
			super(Foo, self).__init__()
			self.value = value
	a = Foo(3)
	b = Foo(3)
	self.assertNotEqual(id(a), id(b))

And here's an example using `__eq__`:

	class Foo(Multiton_OneEquivalentInstance_OnDupRaiseException):
		def __init__(self, value):
			super(Foo, self).__init__()
			self.value = value
		def __eq__(self, other):
			return isinstance(other, self.__class__) and self.value == other.value
	a = Foo(3)
	b = Foo(3)	# will raise a DuplicateInstanceException

#### StartEndWith pattern

This pattern provides some nice functionality that just implementing `__enter__` and `__exit__` doesn't provide.

##### Needing to manually enter and exit

Find yourself implementing `__enter__` and `__exit__`, but still needing to manually call the entrance method and exit method sometimes?
Yes, you can manually call `__enter__` or `__exit__` without using `with`, or you can define other methods like `start` and `end`
which call `__enter__` and `__exit__`. The StartEndWith pattern gives you those nice looking `start` and `end` methods. You can even rename the
methods by passing different method names into the constructor:

	class Foo(StartEndWith):
		def __init__(self):
			super(Foo, self).__init__(methodName_start="begin", methodName_end="end")
		def _start(self, *args, **kwargs):
			<your code to start something>
		def _end(self, *args, **kwargs):
			<your code to end something>
	
	a = Foo()
	a.begin()
	<do something>
	a.end()

##### Telling whether you've began or not

StartEndWith defines an `isActive()` method, which returns whether or not you're inside the `with` statement (or have called `start()`).
Continuing from the example above:

	print(a.isActive())		# False
	a.begin()
	<do something>
	print(a.isActive())		# True
	a.end()
	print(a.isActive())		# False

Or, using `with`:

	with Foo() as a:
		print(a.isActive())		# True

##### Starting more than once without ending

If you'd like to be able to start something more than once without ending it, use `allowStartWhileRunning=True`. (Otherwise, an exception will be raised.)

	class Foo(StartEndWith):
		def __init__(self):
			super(Foo, self).__init__(allowStartWhileRunning=True)
		def _start(self, *args, **kwargs):
			<your code to start something>
		def _end(self, *args, **kwargs):
			<your code to end something>
	
	a.start()
	a.start()
	# this is also valid
	a.end()	# only need to call once

##### Disposable resource

If you only want to be able to call your start and end code (either via explicit calls or using `with`) once and never again, use `useOnce=True`:

	class Foo(StartEndWith):
		def __init__(self):
			super(Foo, self).__init__(useOnce=True)
		def _start(self, *args, **kwargs):
			<your code to start something>
		def _end(self, *args, **kwargs):
			<your code to end something>
	
	a = Foo()
	a.begin()
	<do something>
	a.end()
	a.begin()	# exception is raised
	
	with a:		# exception is raised
		<do something>

## PyPkgUtil

Provides details about python packages and modules. Python can provide a lot of information about a package and a lot of
different ways of loading packages, but the functions and code to accomplish this is scattered and sometimes not obvious.
This `PkgUtil` module provides everything in one location.

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

## Struct

Various structures for holding data.

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

* Sets can't contain duplicate elements
* Sets are unordered
 
However, there are some cases where an ordered set (aka a list with no duplicate elements) is desirable. For this, use
the `OrderedSet` provided here, which provides a similar implementation compared to the built-in `set`, but also provides
methods typically found in a list, such as `insert`/`insertAt`. Refer to the source and unit test for a list of all methods.

	from Lang.Struct import OrderedSet
	set_ = OrderedSet(range(1,10))

## Iter

### Peekable iterator

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

## Diff

### An improved differ

This differ builds upon `difflib.SequenceMatcher` which can diff any python objects with `__eq__` implemented, contained
within a list, tuple, etc. However, the built in class only provides methods for getting matching sets of indices which
refer to matching elements, leaving you to infer which indices don't match. It also doens't give you direct access to
elements that do or don't match. This differ adds all of that functionality. It also fixes:

* A bug: In the built in differ, subsequent calls to `get_matching_blocks()` will return results in a different format due to caching
* Calculating the similarity ratio: The built in differ calculates this ratio taking both diff sides into account, but what's usually wanted is how much one side is similar/different compared to the other side, i.e. `(1 - ratio) / 2 + ratio`

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

* `getmatching()` and `getmismatching()`
  * These return structures with `.block` and `.elems` attributes containing both block indices and the elems which the block refers to
* `get_matching_elems_useOnce()` and `get_mismatching_elems_useOnce()`
  * These are the same as `get_matching_elems()` and `get_mismatching_elems()` except that they are generators instead of functions returning a list

## Concurrency

The `Concurrency` package provides a unified API for locks and semaphores, in addition to some useful utilities.

### @processify

Using this function decorator will automatically cause the function to run inside a new python process:

	from Concurrency.Multiprocessing.decorators import processify
	
	@processify
	def foo():
		<do something>

* Note that the code is not run in parallel to the current process, so this is not for gaining any speed.
* Note that every argument and the return value must be picklable.

### The unified API

Different threading APIs and similar will generally have `lock` and `release` methods, along with possibly some other methods and functionality.
A unified API was made in order to smooth over these differences and fill in functionality that was missing. This includes:

* Standardized method names
* Standardized parameters for `lock` and `release` methods
* Standardized parameters for lock/semaphore constructor

#### @useLock

Using this function decorator will automatically cause a lock to be acquired before executing the function, and released after the function exits:

	from Concurrency.decorators import useLock
	
	lockInstance = 
	@useLock(lockInstance)
	def foo():
		<do something>

## Events

Easy event handling with subscriptions+callbacks, including an API for event logging.

### Events.Proxy

For general event handling involving event subscription and listeners, there is a proxy API. The proxy receives an event
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

## Terminal

Utilities for improving terminal interaction with the user.

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

### An improved ArgParser

In addition to the plethora of features in [python's built-in argparse module](https://docs.python.org/2.7/library/argparse.html), a few more are added in here:

* Improved help formatting, similar to `man`
* Addition of 3 way booleans (`True`, `False`, `None`) and automatic handling of any other iterable type
* Required named parameters - the built in ArgParser only supports required positional arguments and optional named parameters

The new `ArgParser` uses the same interface as the old one, so see the built in `ArgParser` documentation.

Example:

	from Lang.ArgParser import ArgParser
    parser = ArgParser(argument_default=None, add_help=True, description="Adds a user to a linux machine")
    parser.add_argument("username")
	parser.add_argument("-p", "--password", required=False, help="Prompt for password if this is not given")
	parser.add_argument("-H", "--create-home", type=Bool3Way, required=True,
		help="Controls home directory creation for user. None uses the default behavior which varies between machines.")
	args = parser.parse_args()

## DebugTracer

A poor man's debugger. Several arguments are available here. See the source for more details.

	from Lang.DebugTracer import setTraceOn
	setTraceOn()
