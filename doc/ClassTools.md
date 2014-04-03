# <a name="classtools"></a>ClassTools

Various utilities/tools for working with classes. Also includes class patterns.

## Getting the variables of a class instance with `__slots__`

This works the same as the built-in python function `vars()`, except it also works on slotted classes:

	from Lang.ClassTools import vars
	myClassVars = vars(MyClass())

## Patterns

### Keeping track of class instances

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

### Singleton pattern

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

### Multiton pattern

There are two implementations of [the multiton pattern](http://en.wikipedia.org/wiki/Multiton_pattern) aka "registry of singletons",
similar to the singleton pattern above. Although wikipedia says a multiton is simply a singleton that keeps track of instances via key+value
storage, this is very vague. In the py.Lang multiton implementation, each instance of the class must not be equal to another instance of the class
(hence the name `Multiton_OneEquivalentInstance`), else either an exception is raised, or the existing instance, which is equal, is returned
(hence the names `OnDupRaiseException`/`OnDupReturnExisting`, same as the singleton pattern). The uniqueness of the instance can be defined by
the `__eq__` method. However, unlike the singleton pattern, since the instance must be created in order to compare using `__eq__`, be careful
because the object's `__init__` method will always be called, regardless of whether the new instance is equal to an already-created instance.
This could introduce an unintended side effect if not known in advance. If the new instance is not in fact valid, then it will be deleted
(actually garbage collected because it will fall out of scope) after `__init__` and `__eq__` have been called.

The classes which can be inherited from are:
* `Multiton_OneEquivalentInstance_OnDupRaiseException`
* `Multiton_OneEquivalentInstance_OnDupReturnExisting`
  
Here is an example of 2 instances, which are both allowed because the comparison is done by memory address, not using `__eq__`:

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

### StartEndWith pattern

This pattern provides some nice functionality that just implementing `__enter__` and `__exit__` doesn't provide.

#### Needing to manually enter and exit

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

#### Telling whether you've began or not

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

#### Starting more than once without ending

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

#### Disposable resource

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
