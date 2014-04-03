# <a name="events"></a>Events

Easy event handling with subscriptions+callbacks, including an API for event logging.

## Events.Proxy

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

### Handling uncaught exceptions

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

## Event logging

Python has decent built in logging, but it doesn't follow standard object-oriented concepts where methods represent
actions, so the API is not ideal for recording different events in a heavily event based system, as there would need
to be a special, separate call to the logging API for every event. The logging API in `Lang.Events.Logging` fixes this.
It uses the event handling API shown above, where the `Logging` class is an `EventProxy`, and the loggers are
`EventReceiver`s.

### Example using StdoutLogger

This is a very simplistic example of logging to stdout:

	from Lang.Events.Logging import Logging, StdoutLogger
	log = Logging(StdoutLogger)
	log.notifyMyEvent("details", "in", "arguments", "here")

### Example using a custom logger and/or multiple loggers

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
