Package description	{#mainpage}
===================

# Summary of functionality

This package provides a lot of miscellaneous things that probably should have been included in python's built-in
library but weren't, including:

* [FuncTools](#FuncTools.md): Various function/method utilities/tools
	* `FuncTools.Abstraction.abstractmethod`: An abstract method that can be used with `@classmethod`
	* `FuncTools.timeIt`: Timing execution of a function with a decorator
	* `FuncTools.getArgs`: A way to get the argument names and values of a function without using `**kwargs` or `*args`
* [ClassTools](#ClassTools.md): Various utilities/tools for working with classes. Also includes class patterns.
	* `ClassTools.vars`: Getting the variables of a class instance with `__slots__`
	* `ClassTools.Patterns`: A package with implementations of [class patterns](http://en.wikipedia.org/wiki/Software_design_pattern)
		* `ClassTools.Patterns.RegisteredInstances`: Easily keep track of all instances of a class
		* `ClassTools.Patterns.Singleton`: Class bases (using metaclass) that implement the singleton pattern
		* `ClassTools.Patterns.Multiton`: Class bases (using metaclass) that implement the multiton pattern
		* `ClassTools.Patterns.StartEndWith`: Automatic support of the `with` statement by implementing only a start and end method
* [PyPkgUtil](#PyPkgUtil.md): Various module and package utilities/tools (Is a module built in? In what file is it? etc.)
* [Struct](#Struct.md): Implementation of various structures to hold data
	* `Struct.LIFOstack`: LIFO/Stack
	* `Struct.FrozenDict`: Frozen dictionary
	* `Struct.OrderedSet`: Ordered set
* [Iter](#iter)
	* `Iter.PeekableIterable`: A peekable iterator
* [Diff](#Diff.md)
	* `Diff.SequenceMatcher`: An improved differ, based on python's builtin `difflib.SequenceMatcher`
* [Concurrency](#Concurrency.md): Unified API for locks, semaphores, etc., along with some useful tools/utilities
	* `Concurrency.Threading`: A lock and semaphore using standard python threads
	* `Concurrency.FileSystem`: File-system wide concurrency
		* `Concurrency.FileSystem.FileLock_ByFCNTL`: A lock using unix FCNTL file locking
	* `Concurrency.decorators.useLock`: Surround an entire function's execution in a lock
	* `Concurrency.Multiprocessing`: For dealing with multiple python processes
		* `Concurrency.Multiprocessing.decorators.processify`: Run a function in a separate process
* [Terminal](#Terminal.md): Utilities for improving terminal interaction with the user
	* `Terminal.askYesNo`: A simple way of asking user to respond with yes or no
	* `Terminal.FormattedText`: Color text in the terminal. Also can do bold, underline, etc. depending on the terminal.
	* `Terminal.Table`: Nicely prints column+row data in the terminal.
	* `Terminal.ArgParser`: An improved ArgParser for parsing command line arguments
* [Events](#Events.md): Easy event handling with subscriptions+callbacks, including an API for event logging
	* `Events.Proxy`: Provides a super easy API for event subscription and callbacks
	* `Events.Logging`: Skeleton classes for logging events to different destinations
* [DebugTracer](#debugtracer): A poor man's debug tracer when a better tracer isn't available (for example, when running a python script over ssh without remote debugging)

# Miscellaneous

## <a name="iter"></a>Iter

### Peekable Iterator

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

## <a name="debugtracer"></a>DebugTracer

A poor man's debugger. Several arguments are available here. See the source for more details.

	from Lang.DebugTracer import setTraceOn
	setTraceOn()
