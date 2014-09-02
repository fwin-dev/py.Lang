from _singleton_multiton_abstract import _SingletonMultitonAbstract_Meta, DuplicateInstanceException

class _Singleton_Abstract(_SingletonMultitonAbstract_Meta):
	_instances = {}
	def __getattribute__(cls, name):
		"""
		Intercept calls intended for bound methods on the instance, instead of unbound methods on the class.
		@see:	http://stackoverflow.com/questions/53225/how-do-you-check-whether-a-python-method-is-bound-or-not
		@see:	http://bugs.python.org/issue16851#msg181937
		"""
		obj = super(_Singleton_Abstract, cls).__getattribute__(name)
		if hasattr(obj, "__self__") and obj.__self__ == None:		# inspect.ismethod and inspect.isfunction are a little broken in py 2.7 - use this way of detecting methods vs. functions instead
			# then it's a method that expects self as first argument
			if cls in cls.getAllInstances():
				instance = cls.getAllInstances()[cls]
			else:
				instance = cls()	# try to create the instance by using __call__
			return getattr(instance, name)
		return obj


class Singleton_OnDupRaiseException_Meta(_Singleton_Abstract):
	"""
	A singleton allows only one instance of a class, per class/subclass. Upon trying to create a second instance of a class, an exception is raised.
	
		>>> class Foo(object):
		... 	__metaclass__ = Singleton_OnDupRaiseException_Meta
		... 	# your class's code here
		>>> a = Foo()
		>>> b = Foo()
		Traceback (most recent call last):
			...
		DuplicateInstanceException: This class is a singleton, but you tried to create more than one instance
	
	Any method calls (including `__init__`) will be applied to only one instance of the class.
	
	This metaclass also maintains a dictionary of all created classes and the associated instance, thereby also providing a
	"class registration" mechanism. To see which classes have been registered:
	
		>>> Foo.getAllClasses()
		OrderedSet([<class '...Foo'>])
		>>> Foo.getAllInstances()
		{<class '...Foo'>: <...Foo object at 0x...>}
	
	If we were to call these functions before any Foo instance was created, the structures they return would be empty:
	
		>>> class Bar(object):
		... 	__metaclass__ = Singleton_OnDupRaiseException_Meta
		... 	# your class's code here
		>>> Bar.getAllClasses()
		OrderedSet()
		>>> Bar.getAllInstances()
		{}
	
	It is important to note that getAllClasses() is also empty. Even though a class Bar has been specified, the metaclass behind the
	singleton is not yet aware of it. This limitation can be worked around by immediately creating an instance of the singleton after
	the class's definition.
	
	Now let's see what happens when we lose our only reference to the singleton:
	
		>>> class Bar(object):
		... 	__metaclass__ = Singleton_OnDupRaiseException_Meta
		... 	# your class's code here
		>>> Bar()
		<...Bar object at 0x...>
		>>> # more of your code executes
		>>> Bar.getAllInstances()
		{<class '...Bar'>: <...Bar object at 0x...>}	# instance of Bar is still around!
		>>> b = Bar()
		Traceback (most recent call last):
			...
		DuplicateInstanceException: This class is a singleton, but you tried to create more than one instance
	
	So even though you lost the reference, the singleton metaclass internally keeps a reference to the singleton instance. That internal
	reference will always be kept around (weakrefs are not used internally), and it is your responsibility to keep a reference to it for
	yourself. And, if you find that you want to do:
	
		Bar.getAllInstances()[Bar]
	
	frequently, then you should take a look at using Singleton_OnDupReturnExisting_Meta instead.
	
	If the internal reference was **not** always kept around, then, even though only one instance of the class could exist at any single
	point in time, multiple instances could exist over a period of time. We want to avoid this, since re-instantiating a class that intends
	for itself to be a singleton could have unexpected results if the class has some state that it keeps track of. The memory tradeoff
	of holding the instance in RAM indefinitely, until the program terminates, is expected. Therefore, any large amounts of data held onto
	by the instance, for example in an instance variable, should be avoided. If this is your problem, take a look at using a context
	manager: either the builtin python `with` statement, or perhaps Lang.ClassTools.Patterns.StartEndWith
	
	Now let's talk about subclasses. Each subclass of a singleton superclass is also treated as a singleton.
	
		>>> class Foo(object):
		... 	__metaclass__ = Singleton_OnDupRaiseException_Meta
		... 	# your class's code here
		>>> class Bar(Foo):		# Bar is now a subclass of Foo
		... 	__metaclass__ = Singleton_OnDupRaiseException_Meta
		... 	# your class's code here
		>>> a = Foo()
		>>> Foo.getAllClasses()
		OrderedSet([<class '...Foo'>])
		>>> Foo.getAllInstances()
		{<class '...Foo'>: <...Foo object at 0x...>}
		>>> b = Bar()	# creating a Bar singleton does not interfere with the Foo singleton in any way (vice-versa is also true: if we were to create Bar first and then Foo)
		>>> Bar.getAllClasses()		# as expected
		OrderedSet([<class '...Bar'>])
		>>> Bar.getAllInstances()	# as expected
		{<class '...Bar'>: <...Bar object at 0x...>}
		>>> Foo.getAllClasses()
		OrderedSet([<class '...Foo'>, <class '...Bar'>])
		>>> Foo.getAllInstances()
		{<class '...Bar'>: <...Bar object at 0x...>, <class '...Foo'>: <...Foo object at 0x...>}
	
	What just happened? When asked for all classes or instances of the superclass, not only do you get the class/instance reference to the
	superclass, but also all of its subclasses. (And not just direct subclasses either; if we were to subclass Bar, it would also show up.)
	Also notice that getAllClasses() returns an OrderedSet. This order is the same order in which the singletons were first instantiated.
	
	Normally, to get our singleton instance in order to call one of its methods or access its variables, we must pretend like we're
	(re-)instantiating the class, even if we're not. Since this is the primary use case of the singleton, for convenience,
	functions can be called on the singleton directly:
	
		>>> class Foo(object):
		... 	__metaclass__ = Singleton_OnDupRaiseException_Meta
		... 	def eat(self, a, b=2):
		... 		print("eating " + str(a) + " " + str(b))
		>>> Foo.eat(1, 2)		# behind the scenes, the Foo instance is created before eat() is called
		eating 1 2
		>>> Foo.eat(a=3, b=4)	# the Foo instance is already created, so it's looked up behind the scenes and eat() is called on it
		eating 3 4
		>>> Foo.getAllClasses()
		OrderedSet([<class '...Foo'>])
		>>> Foo.getAllInstances()
		{<class '...Foo'>: <...Foo object at 0x...>}
	
	This is the most natural way to use a singleton. And note that we still have access to the metaclass's getAllClasses and
	getAllInstances methods if they are needed. Also note that when Foo is initially created, since we are not actually instantiating it
	by calling it, like `Foo()`, arguments cannot be passed into Foo(...) to initialize it. If your class requires arguments, you can still
	mix and match using Foo() and Foo:
	
		>>> class Foo(object):
		... 	__metaclass__ = Singleton_OnDupRaiseException_Meta
		... 	def __init__(self, value):
		... 		self.value = value
		... 	def eat(self):
		... 		print("eating " + str(self.value))
		>>> Foo("burger").eat()		# explicitly call Foo to create the singleton instance with arguments
		eating burger
		>>> Foo.eat()				# from here on out, we don't have to worry about calling it
		eating burger
	
	http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
	http://stackoverflow.com/questions/392160/what-are-your-concrete-use-cases-for-metaclasses-in-python
	"""
	def __call__(cls, *args, **kwargs):
		if cls in cls._instances.iterkeys():
			raise DuplicateInstanceException("This class is a singleton, but you tried to create more than one instance")
		newInstance = super(Singleton_OnDupRaiseException_Meta, cls).__call__(*args, **kwargs)
		cls._instances[cls] = newInstance
		return newInstance


class Singleton_OnDupReturnExisting_Meta(_Singleton_Abstract):
	"""
	@see	Singleton_OnDupRaiseException_Meta
	
	This metaclass is very similar to Singleton_OnDupRaiseException_Meta, but with one difference. Upon trying to create a second instance of a
	class, no exception is raised; the existing instance (which is kept track of as an internal reference in the metaclass) is returned instead.
	
		>>> class Foo(object):
		... 	__metaclass__ = Singleton_OnDupReturnExisting_Meta
		... 	# your class's code here
		>>> Foo()
		<...Foo object at 0x...>
		>>> memoryAddress = id(Foo.getAllInstances()[Foo])	# let's get the RAM address of the Foo instance, in order to make a point later
		>>> # more of your code executes
		>>> b = Foo()	# oops I lost the reference! let's get it back again
		>>> memoryAddress == id(b)	# yes, it really is a reference to the same instance that we lost before
		True
		>>> Foo.getAllInstances()	# and only one instance was ever created, even though we called Foo() twice
		{<class '...Foo'>: <...Foo object at 0x...>}
	
	http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
	http://stackoverflow.com/questions/392160/what-are-your-concrete-use-cases-for-metaclasses-in-python
	"""
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			newInstance = super(Singleton_OnDupReturnExisting_Meta, cls).__call__(*args, **kwargs)
			cls._instances[cls] = newInstance
		return cls._instances[cls]
